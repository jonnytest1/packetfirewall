
from time import sleep
from termcolor import colored
from os import system
from input import  readInput, stdin_has_content
from log import LogEntry, get_logs

def null():
    pass


class Element:
    
    def __init__(self,text:str,cb=null):
        self.text = text
        self.cb = cb

    def draw(self):
        return self.text




class Row:

    def __init__(self,options:list[Element]):
        self.options=options




class Table:

    def __init__(self,options:list[Row]):
        self.selected_x = 0
        self.selected_y = 0
        self.options=options


    def draw(self):
        buf=""
        for i in range(len(self.options)):
            row=self.options[i]
            for j in range(len(row.options)):
                if i==self.selected_y and j==self.selected_x:
                    buf+=colored(row.options[j].draw(),"black","on_light_grey")
                else:
                    buf+=colored(row.options[j].draw(),"white")
                buf+=" "
            buf+="\r\n"
        return buf

    def right(self):
        self.selected_x+=1
        self.selected_x = min(len(self.options[self.selected_y ].options)-1,self.selected_x)
    def left(self):
        self.selected_x-=1
        self.selected_x = max(0,self.selected_x)

    def down(self):
        self.selected_y+=1
        self.selected_y = min(len(self.options)-1,self.selected_y)
    def up(self):
        self.selected_y-=1
        self.selected_y = max(0,self.selected_y)
    def next(self):
        self.selected_x+=1
        if(self.selected_x > len(self.options[self.selected_y ].options)-1):
            self.selected_x =0
            self.selected_y+=1
        if(self.selected_y> len(self.options)-1):
            self.selected_y =0

    def enter(self):
        el=self.options[self.selected_y].options[self.selected_x]
        if el != None:
            el.cb()

def test():
    r.options.append(Row([Element(str(len(r.options)+1)+"  "),Element("abc")]))

def logs():
    lgs=get_logs()
    print(lgs)


r=Table([
    Row([Element("setup log filter",test),Element("log",logs),Element("abc"),Element("abc"),Element("abc"),Element("abc")]),
    Row([Element("2  "),Element("abc"),Element("abc"),Element("abc"),Element("abc"),Element("abc")]),
    Row([Element("3  "),Element("abc"),Element("abc"),Element("abc"),Element("abc"),Element("abc")])
])


UP_ARROW="\x1b[A"
DOWN_ARROW="\x1b[B"
RIGHT_ARROW="\x1b[C"
LEFT_ARROW="\x1b[D"
CONTROL_CHARACTER="\x1b"

inputbf=""

system("clear")

logids=set()



class LogRow:
    def __init__(self,logRef:LogEntry):
        
        self.row=Row([Element("dst:"+log.dst_ip),Element("dstp:"+log.destination_port),Element("id:"+log.id),Element("srcip:"+log.src_ip),Element("type:"+log.log_type)])
        self.log=logRef
        self.group_ct_el:Element|None=None
        self.group_ct=0


    def add_group(self):
        if self.group_ct_el== None:
            self.group_ct_el=Element("")
            self.row.options.append(self.group_ct_el)
        self.group_ct+=1

        self.group_ct_el.text="grp:"+str(self.group_ct)


  
loglist:list[LogRow]=[]      

while True:
    t=r.draw()
    print(t+"\n\n\n\r")

    hasINput=stdin_has_content(0.2)
    if(hasINput):
        c=readInput()
        inputbf+=c
        if(CONTROL_CHARACTER==inputbf):
            inputbf+=readInput()
            inputbf+=readInput()

        if(inputbf==RIGHT_ARROW):
            r.right()
            inputbf=""
        elif inputbf==LEFT_ARROW:
            r.left()
            inputbf=""
        elif inputbf==DOWN_ARROW:
            r.down()
            inputbf=""
        elif inputbf==UP_ARROW:
            r.up()
            inputbf=""
        elif(inputbf=="\t"):
            r.next()
            inputbf=""
        elif(inputbf=="\r" or inputbf==" "):
            r.enter()
            inputbf=""
        else:
            pass

    duplicatect=0
    newlogs=get_logs()
    for log in newlogs:
        if log.id not in logids:
            logids.add(log.id)

            matched=False
            for logref in loglist:
                if(logref.log.grouped(log)):
                    logref.add_group()
                    matched=True
                    break
            
            if not matched:
                if (log.interface_in == "eth0" or log.interface_in_phys=="eth0") and log.protocol=="TCP" and log.destination_port=="9000":
                    rowRef = LogRow(log)
                    loglist.append(rowRef)
                    r.options.append(rowRef.row)
                
        else:
            duplicatect+=1
        
        

    print(duplicatect)
    system("clear")



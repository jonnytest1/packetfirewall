from queue import Queue
from log import LogEntry, get_logs
from ui.baseelement import UITextElement
from ui.ui import UI
from ui.ui_textbutton_element import UITextButton



logids=set()
  

class LogRow:
    def __init__(self,log:LogEntry):
        
        self.row:list[UITextElement] =[]
        for field in LogEntry.MATCHING_PROPS_FOR_GROUP:
            self.row.append(UITextButton(f"{field}:{log.prop_dict[field]}"))
            #UITextButton("dst:"+log.dst_ip),UITextButton("dstp:"+log.destination_port),UITextButton("id:"+log.id),UITextButton("srcip:"+log.src_ip),UITextButton("type:"+log.log_type)
        self.log=log
        self.group_ct_el:UITextButton|None=None
        self.group_ct=0

        self.latest_el:UITextButton|None=None


    def add_group(self,other:LogEntry):
        if self.group_ct_el== None:
            self.group_ct_el=UITextButton("")
            self.row.append(self.group_ct_el)
        self.group_ct+=1

        self.group_ct_el.text="grp:"+str(self.group_ct)

        if self.latest_el == None:
            self.latest_el=UITextButton("")
            self.row.append(self.latest_el)


        self.latest_el.text="latest:"+other.datetime.isoformat()


loglist:list[LogRow]=[]      

def log_loop(ui:UI,evt_quque:Queue):
    while True:
        if(not evt_quque.empty()):
            evt=evt_quque.get()
            if(evt=="QUIT"):
                return

        newlogs=get_logs()
        for log in newlogs:
            if log.id not in logids:
                logids.add(log.id)

                matched=False
                for logref in loglist:
                    if(logref.log.grouped(log)):
                        logref.add_group(log)
                        ui.redraw()
                        matched=True
                        break
                
                if not matched:
                    if (log.interface_in == "eth0" or log.interface_in_phys=="eth0") and log.protocol=="TCP" and log.destination_port=="9000":
                        row_ref = LogRow(log)
                        loglist.append(row_ref)
                        ui.columns.append(row_ref.row)
                        ui.redraw()
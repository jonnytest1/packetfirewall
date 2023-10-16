from datetime import datetime
from queue import Queue
from log import LogEntry, get_logs
from ui.baseelement import UITextElement
from ui.ui import UI
from ui.ui_textbutton_element import UITextButton



logids=set()
  

class LogRow:
    FIRST_DETAIL_INSET="     "

    def __init__(self,log:LogEntry):
        
        self.row:list[UITextElement] =[]
        self.row.append(UITextButton(f"id:{log.prop_dict['id']}"))
        self.log_id=log.id
        self.log_type=log.log_type
        self.log_time=log.datetime.timestamp()


        self.detail_row:list[UITextElement]=[]
        self.detail_row.append(UITextButton(LogRow.FIRST_DETAIL_INSET+self.log_type.replace("LOG_INTERCEPT#","")))

        for field in LogEntry.MATCHING_PROPS_FOR_GROUP:
            self.row.append(UITextButton(f"{field}:{log.prop_dict[field]}"))
        
        self.log=log
        self.group_ct_el:UITextButton|None=None
        self.group_ct=0

        self.latest_el:UITextButton|None=None
        self.steps_el:UITextButton|None=None


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

        if self.steps_el == None:
            self.steps_el=UITextButton("")
            self.row.append(self.steps_el)
            
        
        if other.datetime.timestamp()>(self.log_time+(5)):
            self.log_id=other.id
            self.log_type=other.log_type
            self.log_time=other.datetime.timestamp()
            self.detail_row.clear()
            self.detail_row.append(UITextButton(LogRow.FIRST_DETAIL_INSET+other.log_type.replace("LOG_INTERCEPT#","")))



        if(other.id==self.log_id):
            if(other.log_type != self.log_type):
                self.detail_row.append(UITextButton(other.log_type.replace("LOG_INTERCEPT#","")))

        pass


loglist:list[LogRow]=[]      

def log_loop(ui:UI,evt_quque:Queue):
    starttime=datetime.now()
    while True:
        if(not evt_quque.empty()):
            evt=evt_quque.get()
            if(evt=="QUIT"):
                return

        newlogs=get_logs()
        for log in newlogs:
            
            try:
                if log.datetime<starttime:
                    continue
                if log.log_type.startswith("LOG_INTERCEPT"):
                    setid=log.id+log.log_type
                    if setid not in logids:
                        logids.add(setid)

                        matched=False
                        for logref in loglist:
                            if(logref.log.grouped(log)):
                                logref.add_group(log)
                                ui.redraw()
                                matched=True
                                break
                        
                        if not matched:
                            row_ref = LogRow(log)
                            loglist.append(row_ref)
                            ui.columns.append(row_ref.row)
                            ui.columns.append(row_ref.detail_row)
                            ui.redraw()
            except Exception as e:
                pass

                    
from datetime import datetime
from queue import Queue
from forms.log_form import LogForm
from log import LogEntry, get_logs
from ui.baseelement import UITextElement
from ui.ui import UI
from ui.ui_textbutton_element import UITextButton

logids=set()
  
def log_loop(log_form:LogForm,evt_quque:Queue):
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

                        log_form.add_log(log)
            except Exception as e:
                pass

                    
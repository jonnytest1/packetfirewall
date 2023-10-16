from forms.log_row import LogRow
from log import LogEntry
from ui.ui import UI


class LogForm:

    def __init__(self,ui:UI):
        self.ui=ui
        self.loglist:list[LogRow]=[]   


    def add_log(self,log:LogEntry):
        matched=False
        for logref in self.loglist:
            if(logref.log.grouped(log)):
                logref.add_group(log)
                self.ui.redraw()
                matched=True
                break
        
        if not matched:
            row_ref = LogRow(log)
            self.loglist.append(row_ref)
            self.ui.columns.append(row_ref.row)
            self.ui.columns.append(row_ref.detail_row)
            self.ui.redraw()



    

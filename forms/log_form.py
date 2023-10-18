from forms.log_row import LogRow
from log import LogEntry
from ui.ui import UI
from ui.ui_view import ui_view


class LogForm:

    def __init__(self,view:ui_view):
        self.view=view
        self.loglist:list[LogRow]=[]   


    def add_log(self,log:LogEntry):
        matched=False
        for logref in self.loglist:
            if(logref.log.grouped(log)):
                logref.add_group(log)
                self.view.redraw()
                matched=True
                break
        
        if not matched:
            row_ref = LogRow(log)
            self.loglist.append(row_ref)
            self.view.columns.append(row_ref.row)
            self.view.columns.append(row_ref.detail_row)
            self.view.redraw()



    

from api.model.log_entry import LogEntry
from forms.add_rule_form import add_rule_form
from ui.baseelement import UITextElement
from ui.ui_textbutton_element import UITextButton


class LogRow:
    FIRST_DETAIL_INSET="     "

    def __init__(self,log:LogEntry):
        
        self.row:list[UITextElement] =[]
        self.row.append(UITextButton(f"id:{log.prop_dict['id']}"))
        self.log_id=log.id
        self.log_type=log.log_type
        self.log_time=log.datetime.timestamp()
        self.assigned_log=log


        self.detail_row:list[UITextElement]=[]
        self.detail_row.append(UITextButton(LogRow.FIRST_DETAIL_INSET+self.log_type.replace("LOG_INTERCEPT#",""),self.click_fnc))

        for field in LogEntry.MATCHING_PROPS_FOR_GROUP:
            self.row.append(UITextButton(f"{field}:{log.prop_dict[field]}"))
        
        self.log=log
        self.group_ct_el:UITextButton|None=None
        self.group_ct=0

        self.latest_el:UITextButton|None=None
        self.steps_el:UITextButton|None=None

    def click_fnc(self,txt):
        add_rule_form(self.assigned_log)

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
        
        if other.datetime.timestamp()>(self.log_time+(5)):
            self.log_id=other.id
            self.log_type=other.log_type
            self.log_time=other.datetime.timestamp()
            self.assigned_log=other
            self.detail_row.clear()
            self.detail_row.append(UITextButton(LogRow.FIRST_DETAIL_INSET+other.log_type.replace("LOG_INTERCEPT#",""),self.click_fnc))



        if(other.id==self.log_id):
            if(other.log_type != self.log_type):
                self.detail_row.append(UITextButton(other.log_type.replace("LOG_INTERCEPT#",""),self.click_fnc))

        pass
  
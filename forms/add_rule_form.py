from log import LogEntry
from forms.ui_ref import ui_element
from ui.ui import UI
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton



class AddForm:
    def __init__(self,prop:LogEntry):
        self.log=prop
        self.mode_selected=False
        self.ui:UI

    def mode_select(self,mode):
        self.mode_selected=mode
            
        if mode== "DNAT":
            self.ui.columns.insert(len(self.ui.columns)-1,[UITextButton("target-port: "),UITextInput("__dest_port__")])
            self.ui.columns.insert(len(self.ui.columns)-1,[UITextButton("target-ip: "),UITextInput("__dest_ip__")])

    def done(self,_):
        errors=self.validate()
        if len(errors):
            for error in errors:
                btn = UITextButton(error)
                btn.background_color="on_red"
                self.ui.columns.insert(len(self.ui.columns)-1,[btn])
            
        else:
            self.ui.back()

    def add_to(self,ui:UI):
        self.ui=ui
        ui.columns.append([UITextButton("mode:"),UITextButton("DROP",self.mode_select),UITextButton("ACCEPT",self.mode_select),UITextButton("DNAT",self.mode_select)])
        ui.columns.append([UITextButton("done",self.done )])


    def validate(self):
        errors=[]
        errors.append("example error")

        return errors





def add_rule_form(log:LogEntry):
    ui_element.set_columns([[UITextButton("back")]])
    form=AddForm(log)
    form.add_to(ui_element)
    pass
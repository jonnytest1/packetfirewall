from log import Log_Rule_Condition, IpTablesRule, LogEntry, add_rule
from forms.ui_ref import ui_element
from ui.ui import UI
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton
from ui.ui_view import ui_view



class AddForm:
    def __init__(self,prop:LogEntry):
        self.log=prop
        self.mode_selected=False
        self.ui:UI
        self.add_view=ui_view()
        self.dst_ip:UITextInput

    def mode_select(self,mode):
        self.mode_selected=mode
            
        if mode== "DNAT":
            self.dnat_dst_port = UITextInput("__dest_port__")
            self.add_view.columns.insert(len(self.add_view.columns)-1,[UITextButton("dnat-target-port: "),self.dnat_dst_port])
            self.dst_ip = UITextInput("__dest_ip__")
            self.dst_ip.placeholder=self.log.dst_ip
            self.dst_ip.use_placeholder=True
            self.add_view.columns.insert(len(self.add_view.columns)-1,[UITextButton("dnat-target-ip: "),self.dst_ip])

        
        self.add_view.columns.insert(len(self.add_view.columns)-1,[UITextButton("")])
        self.add_view.columns.insert(len(self.add_view.columns)-1,[UITextButton("conditions:")])
        self.dst_port_cnd= UITextInput("__dest_port_condition__")
        self.dst_port_cnd.placeholder=self.log.destination_port
        self.dst_port_cnd.use_placeholder=True
        self.add_view.columns.insert(len(self.add_view.columns)-1,[UITextButton("destination-port:"), self.dst_port_cnd])

    def done(self,_):
        errors=self.validate()
        if len(errors):
            for error in errors:
                btn = UITextButton(error)
                btn.background_color="on_red"
                self.add_view.columns.insert(len(self.add_view.columns)-1,[btn])
            
        else:

            rule=IpTablesRule("nat")

            dport=self.dst_port_cnd.text
            if dport == None:
                dport=self.log.destination_port
            
            rule.propsdict["dst_port"]=Log_Rule_Condition("dst_port",dport,False)
            
            rule.propsdict["chain"]=Log_Rule_Condition("chain","PREROUTING",False)
            rule.propsdict["jump"]=Log_Rule_Condition("jump","DNAT",False)
            if self.dst_ip.text == None:
                self.dst_ip.text=self.log.dst_ip
            rule.propsdict["nat_dst_ip"]=Log_Rule_Condition("nat_dst_ip",f"{self.dst_ip.text}:{self.dnat_dst_port.text}",False)

            if rule.propsdict["dst_port"] and "protocol" not in rule.propsdict:
                rule.propsdict["protocol"]=Log_Rule_Condition("protocol","tcp",False)

            if self.mode_selected=="DNAT":
                
                add_rule(rule)
            self.ui.back()

    def add_to(self,ui:UI):
        self.ui=ui
        self.add_view.columns.append([UITextButton("mode:"),UITextButton("DROP",self.mode_select),UITextButton("ACCEPT",self.mode_select),UITextButton("DNAT",self.mode_select)])
        self.add_view.columns.append([UITextButton("done",self.done )])

        


    def validate(self):
        errors=[]
        #errors.append("example error")

        return errors





def add_rule_form(log:LogEntry):
    form=AddForm(log)
    form.add_view.columns.append([UITextButton("back")])
    form.add_to(ui_element)

    ui_element.set_view(form.add_view)
    
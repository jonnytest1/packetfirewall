from forms.graph import to_graph
from forms.rules import display_rules
from log import Log_Rule_Condition, cleanup_logging, setup_logging
from ui.form import UIForm
from forms.ui_ref import ui_element
from ui.ui_textbutton_element import UITextButton
from ui.ui_view import ui_view


DESTINATION_PORT_FORM="destination port"
DESTINATION_IP_FORM="destination ip"
SRC_IP_FORM="source ip"
SRC_IF_FORM="source interface"


def onfilter_form(dict):
    #cleanup_logging()
    conditions=[Log_Rule_Condition("protocol","tcp",False)]
    if dict[DESTINATION_PORT_FORM]!=None:
        conditions.append(Log_Rule_Condition(Log_Rule_Condition.DESTINATION_PORT,dict[DESTINATION_PORT_FORM],False))
    
    setup_logging(conditions)
    

class main_view(ui_view):

    def __init__(self):
        super(main_view,self).__init__()
        self.form=UIForm(fields=[SRC_IF_FORM,SRC_IP_FORM,DESTINATION_IP_FORM,DESTINATION_PORT_FORM]
            ,confirmationname="setup log filter",oncomplete=onfilter_form)


main_form_instance=main_view()
main_form_instance.columns.append([UITextButton("set filters for packets you're interested in",to_graph)])
main_form_instance.form.add_to(main_form_instance)
main_form_instance.columns.append([UITextButton("graph",to_graph)])
main_form_instance.columns.append([UITextButton("rules",display_rules)])

def main_form():
    global main_form_instance
    ui_element.set_view(main_form_instance)
    return main_form_instance
    
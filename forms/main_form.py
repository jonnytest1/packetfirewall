from forms.graph import to_graph
from forms.rules import display_rules
from log import Condition, cleanup_logging, setup_logging
from ui.form import UIForm
from forms.ui_ref import ui_element
from ui.ui_textbutton_element import UITextButton

DESTINATION_PORT_FORM="destination port"
DESTINATION_IP_FORM="destination ip"
SRC_IP_FORM="source ip"
SRC_IF_FORM="source interface"


def onfilter_form(dict):
    cleanup_logging()
    conditions=[Condition("protocol","tcp",False)]
    if dict[DESTINATION_PORT_FORM]!=None:
        conditions.append(Condition(Condition.DESTINATION_PORT,dict[DESTINATION_PORT_FORM],False))
    
    setup_logging(conditions)
    



form=UIForm(fields=[SRC_IF_FORM,SRC_IP_FORM,DESTINATION_IP_FORM,DESTINATION_PORT_FORM]
            ,confirmationname="setup log filter",oncomplete=onfilter_form)



def main_form():
    ui_element.set_columns([])
    ui_element.columns.append([UITextButton("set filters for packets you're interested in",to_graph)])
    form.add_to(ui_element)
    ui_element.columns.append([UITextButton("graph",to_graph)])
    ui_element.columns.append([UITextButton("rules",display_rules)])
    
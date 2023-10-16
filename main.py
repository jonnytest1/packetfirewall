
from threading import Thread
from time import sleep
from termcolor import colored
from os import system
from input.input import  input_loop, stdin_has_content
from input.input_types import INPUT_TYPES
from log import Condition, LogEntry, cleanup_logging, get_logs, get_rules, setup_logging
from log_reader import log_loop
from ui.baseelement import UITextElement
from ui.form import UIForm
from ui.ui import UI
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton
from queue import Empty, Queue 
import sys


def logs():
    lgs=get_logs()
    print(lgs)


ui=UI()


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

def remove_filters():
    print("cleaning up log filters...\r")
    cleanup_logging()
    print("done\r")

form=UIForm(fields=[SRC_IF_FORM,SRC_IP_FORM,DESTINATION_IP_FORM,DESTINATION_PORT_FORM]
            ,confirmationname="setup log filter",oncomplete=onfilter_form)


def main_escape():
    stop_flag_input.put("QUIT")
    stop_flag_log.put("QUIT")
    remove_filters()
    print("one more input to reactivate input thread(it doesnt know its supposed to stop otherwise 😅) \r")
    log_thread.join()
    input_thread.join()
    return True

escape_fnc=main_escape

def to_form():
    global escape_fnc
    ui.set_columns([])
    ui.columns.append([UITextButton("set filters for packets you're interested in",to_graph)])
    form.add_to(ui)
    ui.columns.append([UITextButton("graph",to_graph)])
    ui.columns.append([UITextButton("rules",to_rules)])
    escape_fnc=main_escape



def to_rules():
    rules=get_rules()
    ui.set_columns([[UITextButton("back",to_form)]])

    for rule in rules:
        chain=rule.propsdict["chain"]
        row:list[UITextElement] = [UITextButton(f"table:{rule.table}"),UITextButton(f"chain:{chain.value}")]
        for key,val in rule.propsdict.items():
            if key!="chain":
                row.append(UITextButton(f"{key}:{val.value}",rule.delete))
        ui.columns.append(row)

def to_graph():
    global escape_fnc
    ui.set_columns([[UITextButton("back",to_form),UITextButton(""" src: https://serverfault.com/questions/1008556/is-there-a-need-for-the-nat-table-input-chain
*external packet* 
      ↓
 raw-PREROUTING                                                                *local packet*
      ↓                                                                             ↓
mangle-PREROUTNG                                                                raw-OUTPUT
      ↓                                                                             ↓
src_ip 127.0.0.1? No→ nat-PREROUTING                                           mangle-OUTPUT
   Yes|                    ↓                                                        ↓
      |               dst_ip 127.0.0.1? No→ mangle-FORWARD                      nat-OUTPUT 
      |                 Yes↓                     ↓                                  ↓
      --------------→ mangle-INPUT          filter-FORWARD                    filter-OUTPUT
                           ↓                     ↓                                  ↓
                      filter-INPUT         security-FORWARD                  security-OUTPUT
                           ↓                     |                                  |
                     security-INPUT              ----→ [Release to interface_out]←---
                           ↓                                       ↓
                        nat-INPUT                           mangle-POSTROUTING
                           ↓                                       ↓                   
                      *LOCAL(apps)*                         dst_ip 127.0.0.1? No------↓            
                                                                   |             nat-POSTROUTING
                                                                   |------------------|
                                                                   ↓
                                                                 *OUT*
""",to_form)]])
    escape_fnc=to_form

to_form()

inputbf=""

stop_flag_log=Queue()
stop_flag_input=Queue()

log_thread=Thread(target=log_loop,args=(ui,stop_flag_log))
log_thread.start()

input_Events=Queue()
input_thread=Thread(target=input_loop,args=(input_Events,stop_flag_input))
input_thread.start()

while True:
    ui.redraw()

    #hasINput=stdin_has_content(1)
    #if(hasINput):
    c=input_Events.get()
    inputbf+=c
    if(INPUT_TYPES.CONTROL_CHARACTER==inputbf):
        try:
            inputbf+=input_Events.get(timeout=0.1)
            inputbf+=input_Events.get()
        except Empty as e:
            inputbf=INPUT_TYPES.ESCAPE_MAPPED

    if(ui.focused):
        should_unfocus=ui.focused.event(inputbf)
        
        inputbf=""
        if(should_unfocus):
            ui.focused.blur()
            ui.focused=None

        continue
    

    if(inputbf==INPUT_TYPES.RIGHT_ARROW):
        ui.right()
        inputbf=""
    elif inputbf==INPUT_TYPES.LEFT_ARROW:
        ui.left()
        inputbf=""
    elif inputbf==INPUT_TYPES.DOWN_ARROW:
        ui.down()
        inputbf=""
    elif inputbf==INPUT_TYPES.UP_ARROW:
        ui.up()
        inputbf=""
    elif(inputbf=="\t"):
        ui.next()
        inputbf=""
    elif(inputbf=="\r" or inputbf==" "):
        ui.enter()
        inputbf=""
    elif(inputbf==INPUT_TYPES.ESCAPE_MAPPED):
        if escape_fnc()== True:
            break
        inputbf=""
    else:
        pass



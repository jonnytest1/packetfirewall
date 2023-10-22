
from threading import Thread
from api.iptables import ip_tables
from forms.log_form import LogForm
from forms.main_form import DESTINATION_PORT_FORM, main_form
from input.input import  input_loop
from input.input_types import INPUT_TYPES
from log_reader import log_loop
from forms.ui_ref import ui_element
from queue import Empty, Queue 
from tables_api import tables_api


ui=ui_element

def remove_filters():
    print("cleaning up log filters...\r")
    tables_api.cleanup_logging()
    print("done\r")

def main_escape():
    stop_flag_input.put("QUIT")
    stop_flag_log.put("QUIT")
    remove_filters()
    print("one more input to reactivate input thread(it doesnt know its supposed to stop otherwise 😅) \r")
    log_thread.join()
    input_thread.join()
    return True

ui.escape_fnc=main_escape

  
main_instance=main_form()

inputbf=""

stop_flag_log=Queue()
stop_flag_input=Queue()


log_form=LogForm(main_instance)

log_thread=Thread(target=log_loop,args=(log_form,stop_flag_log))
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
        went_back=ui.back()
        if went_back== False:
            main_escape()
            break
        inputbf=""
    else:
        pass



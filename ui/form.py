from typing import Callable
from ui.ui import UI
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton
from ui.ui_view import ui_view

FormResponse=dict[str,str|None]



class UIForm():

    def __init__(self,fields:list[str],confirmationname:str,oncomplete:None|Callable[[FormResponse],None]=None):
        self.complete=oncomplete
        self.fields=fields
        self.confirmationname=confirmationname
        self.uidict:dict[str,UITextInput]=dict()

    
    def add_to(self,ui:ui_view):
        for field in self.fields:
            fieldinput=UITextInput(field)
            self.uidict[field]=fieldinput
            ui.columns.append([UITextButton(f"{field}:"),fieldinput])

        
        def completion(txt):
            result:FormResponse=dict()
            
            for field in self.fields:
                result[field]=self.uidict[field].text

            if self.complete != None:
                self.complete(result)
            

        ui.columns.append([UITextButton(self.confirmationname,completion)])
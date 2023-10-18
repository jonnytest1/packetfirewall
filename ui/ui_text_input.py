
from termcolor import RESET, colored
from ui.baseelement import UITextElement
from input.input_types import INPUT_TYPES



class UITextInput(UITextElement):
    FOREGROUND_COLOR="white"
    BACKGROUND_COLOR="on_black"

    def __init__(self,placeholder:str,cb=None):
        self.placeholder = placeholder
        self.cb = cb
        self.text:str|None=None
        self.text_before_focus=""
        self.selection=0
        self.focused=False
        self.use_placeholder=False

    def focus(self):
        self.focused=True
        self.text_before_focus=self.text
        if self.text == None:
            if(self.use_placeholder):
                self.text=self.placeholder
            else:
                self.text=""
            self.selection=0
    def blur(self):
        self.focused=False


    def event(self,evt:str):
        if(self.text==None):
            self.text=""

        if(evt=="\r"):
            if self.cb != None:
                self.cb(self.text)
            return True
        elif(evt=="ESCAPE"):
            self.text=self.text_before_focus
            return True
        elif(evt==INPUT_TYPES.BACK_SPACE):
            self.text=self.text[0:-1]
            self.selection-=1
            return
        elif(evt==INPUT_TYPES.LEFT_ARROW):
            self.selection-=1
            return
        elif(evt==INPUT_TYPES.RIGHT_ARROW):
            self.selection+=1
            self.selection=min(self.selection,len(self.text))
            return
        elif(evt.startswith(INPUT_TYPES.CONTROL_CHARACTER)):
            return
        [front,back]=[self.text[0:self.selection],self.text[self.selection:]]
        self.text=front+evt+back
        self.selection+=1

    def terminal_representation(self):
        if(self.text==None):
            return colored(self.placeholder,attrs=["underline"])
        
        if len(self.text)==0 or not self.focused:
            return colored(self.text,attrs=["bold"])
        [front,selection,back]=[self.text[0:self.selection-1],self.text[self.selection-1],self.text[self.selection:]]

        front_fmt=colored(front,UITextInput.FOREGROUND_COLOR,attrs=["bold"])
        back_fmt= colored(back ,UITextInput.FOREGROUND_COLOR,attrs=["bold"])
        selection_fmt=colored(selection,UITextInput.FOREGROUND_COLOR,attrs=["bold","underline"])
        return RESET+front_fmt+selection_fmt+back_fmt

    def terminal_representation_length(self):
        if(self.text==None):
            return len(self.placeholder)
        return len(self.text)



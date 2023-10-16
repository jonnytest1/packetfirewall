from typing import Callable

from termcolor import colored,RESET
from ui.baseelement import UITextElement


ButtonCallback=Callable[[str],None]

class UITextButton(UITextElement):
    def __init__(self,text:str,cb:None|ButtonCallback=None):
        self.text = text
        self.cb = cb
        self.color:str|None=None
        self.background_color:str|None=None

    def call(self):
        if self.cb != None:
            self.cb(self.text);
    def terminal_representation(self):
        if(self.color!= None or self.background_color != None):
            return RESET+colored(self.text,color=self.color,on_color=self.background_color)
        return self.text
    def terminal_representation_length(self):
        return len(self.text)
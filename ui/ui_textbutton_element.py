from ui.baseelement import UITextElement


class UITextButton(UITextElement):
    def __init__(self,text:str,cb=None):
        self.text = text
        self.cb = cb

    def call(self):
        if self.cb != None:
            self.cb();
    def terminal_representation(self):
        return self.text
    def terminal_representation_length(self):
        return len(self.text)
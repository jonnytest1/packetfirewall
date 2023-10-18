


from abc import ABC,abstractproperty

from ui.baseelement import UITextElement


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.ui import UI

class ui_view:

    def __init__(self):
        self.columns:list[list[UITextElement]] = []
        self.ui_ref:"UI"
        self.active:bool
        # ...

    def redraw(self):
        if(self.active):
            self.ui_ref.redraw()


  

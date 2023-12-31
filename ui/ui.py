from math import ceil
from os import system
from typing import Callable
from termcolor import COLORS, colored,RESET

from ui.baseelement import UITextElement
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton
from ui.ui_view import ui_view

ESCAPE_FNC=Callable[[],bool|None]

class UI:
    DEFAULT_BACKGROUND="on_black"

    def __init__(self):
        #self.columns:list[list[UITextElement]]=[]
        self.view:ui_view
        self.history:list[ui_view]=[]
        self.selected_x = 0
        self.selected_y = 0
        self.focused=None
        self.escape_fnc:ESCAPE_FNC

    def terminal_representation(self):
        buf=""
        cols=self.view.columns
        for i in range(len(cols)):
            row=cols[i]
            for j in range(len(row)):
                if i==self.selected_y and j==self.selected_x:
                    buf+=colored(row[j].terminal_representation(),"black","on_light_grey")
                else:
                    buf+=colored(RESET+row[j].terminal_representation(),"white")
                buf+=" "
            buf+="\r\n"
        return buf

    def set_view(self,view:ui_view):
        if hasattr(self,"view"):
            self.view.active=False
            self.history.append(self.view)

        self.view=view
        self.view.ui_ref=self
        self.view.active=True
        self.selected_x=0
        self.selected_y=0

    def back(self):
        self.selected_x=0
        self.selected_y=0
        if len(self.history) ==0:
            return False
        self.view.active=False
        self.view=self.history.pop()
        self.view.active=True

    def redraw(self):
        system("clear")
        ui_strt=self.terminal_representation()
        print(ui_strt.replace("\n","\r\n")+"\n\n\n\r")
    
    def right(self):
        self.selected_x+=1
        self.selected_x = min(len(self.view.columns[self.selected_y ])-1,self.selected_x)
    def left(self):
        self.selected_x-=1
        self.selected_x = max(0,self.selected_x)

    def down(self):
        current_column= self.selected_y
        self.selected_y+=1
        self.selected_y = min(len(self.view.columns)-1,self.selected_y)
        offset_left=0
        for i in range(self.selected_x):
            offset_left+=self.view.columns[current_column][i].terminal_representation_length()+1
        offset_left+=ceil(self.view.columns[current_column][self.selected_x].terminal_representation_length()/2)
        new_x=0
        new_i=0
        newcolumn=self.view.columns[self.selected_y]
        for i in range(len(newcolumn)):
            if new_x+newcolumn[i].terminal_representation_length()+1 < offset_left:
                new_x+=newcolumn[i].terminal_representation_length()+1
                new_i=i+1
            else:
                break
        self.selected_x=new_i
        self.selected_x = min(len(self.view.columns[self.selected_y ])-1,self.selected_x)
    def up(self):
        current_column= self.selected_y
        self.selected_y-=1
        self.selected_y = max(0,self.selected_y)
        self.selected_y = min(len(self.view.columns)-1,self.selected_y)
        offset_left=0
        for i in range(self.selected_x):
            offset_left+=self.view.columns[current_column][i].terminal_representation_length()+1
        offset_left+=ceil(self.view.columns[current_column][self.selected_x].terminal_representation_length()/2)
        new_x=0
        new_i=0
        newcolumn=self.view.columns[self.selected_y]
        for i in range(len(newcolumn)):
            if new_x+newcolumn[i].terminal_representation_length()+1 < offset_left:
                new_x+=newcolumn[i].terminal_representation_length()+1
                new_i=i+1
            else:
                break
        self.selected_x=new_i
        self.selected_x = min(len(self.view.columns[self.selected_y ])-1,self.selected_x)
        

    def next(self):
        self.selected_x+=1
        if(self.selected_x > len(self.view.columns[self.selected_y ])-1):
            self.selected_x =0
            self.selected_y+=1
        if(self.selected_y> len(self.view.columns)-1):
            self.selected_y =0

    def get_selected(self):
        return self.view.columns[self.selected_y][self.selected_x]

    def enter(self):
        el=self.get_selected()
        if el != None :
            if isinstance(el,UITextButton):
                if el.text=="back" and el.cb == None:
                    self.back()
                else:
                    el.call()
            elif isinstance(el,UITextInput):
                self.focused=el
                el.focus()


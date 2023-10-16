from math import ceil
from os import system
from typing import Callable
from termcolor import COLORS, colored,RESET

from ui.baseelement import UITextElement
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton

ESCAPE_FNC=Callable[[],bool|None]

class UI:
    DEFAULT_BACKGROUND="on_black"

    def __init__(self):
        self.columns:list[list[UITextElement]]=[]
        self.history=[]
        self.selected_x = 0
        self.selected_y = 0
        self.focused=None
        self.escape_fnc:ESCAPE_FNC

    def terminal_representation(self):
        buf=""
        for i in range(len(self.columns)):
            row=self.columns[i]
            for j in range(len(row)):
                if i==self.selected_y and j==self.selected_x:
                    buf+=colored(row[j].terminal_representation(),"black","on_light_grey")
                else:
                    buf+=colored(RESET+row[j].terminal_representation(),"white")
                buf+=" "
            buf+="\r\n"
        return buf

    def set_columns(self,cols:list[list[UITextElement]]):
        if len(self.columns):
            self.history.append(self.columns)
        self.columns=cols
        self.selected_x=0
        self.selected_y=0

    def back(self):
        self.selected_x=0
        self.selected_y=0
        if len(self.history) ==0:
            return False
        self.columns=self.history.pop()

    def redraw(self):
        system("clear")
        ui_strt=self.terminal_representation()
        print(ui_strt.replace("\n","\r\n")+"\n\n\n\r")
    
    def right(self):
        self.selected_x+=1
        self.selected_x = min(len(self.columns[self.selected_y ])-1,self.selected_x)
    def left(self):
        self.selected_x-=1
        self.selected_x = max(0,self.selected_x)

    def down(self):
        current_column= self.selected_y
        self.selected_y+=1
        self.selected_y = min(len(self.columns)-1,self.selected_y)
        offset_left=0
        for i in range(self.selected_x):
            offset_left+=self.columns[current_column][i].terminal_representation_length()+1
        offset_left+=ceil(self.columns[current_column][self.selected_x].terminal_representation_length()/2)
        new_x=0
        new_i=0
        newcolumn=self.columns[self.selected_y]
        for i in range(len(newcolumn)):
            if new_x+newcolumn[i].terminal_representation_length()+1 < offset_left:
                new_x+=newcolumn[i].terminal_representation_length()+1
                new_i=i+1
            else:
                break
        self.selected_x=new_i
        self.selected_x = min(len(self.columns[self.selected_y ])-1,self.selected_x)
    def up(self):
        current_column= self.selected_y
        self.selected_y-=1
        self.selected_y = max(0,self.selected_y)
        self.selected_y = min(len(self.columns)-1,self.selected_y)
        offset_left=0
        for i in range(self.selected_x):
            offset_left+=self.columns[current_column][i].terminal_representation_length()+1
        offset_left+=ceil(self.columns[current_column][self.selected_x].terminal_representation_length()/2)
        new_x=0
        new_i=0
        newcolumn=self.columns[self.selected_y]
        for i in range(len(newcolumn)):
            if new_x+newcolumn[i].terminal_representation_length()+1 < offset_left:
                new_x+=newcolumn[i].terminal_representation_length()+1
                new_i=i+1
            else:
                break
        self.selected_x=new_i
        self.selected_x = min(len(self.columns[self.selected_y ])-1,self.selected_x)
        

    def next(self):
        self.selected_x+=1
        if(self.selected_x > len(self.columns[self.selected_y ])-1):
            self.selected_x =0
            self.selected_y+=1
        if(self.selected_y> len(self.columns)-1):
            self.selected_y =0

    def get_selected(self):
        return self.columns[self.selected_y][self.selected_x]

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


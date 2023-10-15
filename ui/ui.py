from math import ceil
from os import system
from termcolor import COLORS, colored,RESET

from ui.baseelement import UITextElement
from ui.ui_text_input import UITextInput
from ui.ui_textbutton_element import UITextButton


class UI:
    DEFAULT_BACKGROUND="on_black"

    def __init__(self):
        self.columns:list[list[UITextElement]]=[]
        self.selected_x = 0
        self.selected_y = 0
        self.focused=None

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
        self.columns=cols
        self.selected_x=0
        self.selected_y=0

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
                el.call()
            elif isinstance(el,UITextInput):
                self.focused=el
                el.focus()


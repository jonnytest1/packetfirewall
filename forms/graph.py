from ui.ui_textbutton_element import UITextButton

from forms.ui_ref import ui_element
from ui.ui_view import ui_view


graph_view=ui_view()

def back(_):
        ui_element.back()

graph_view.columns.append([UITextButton("back"),UITextButton(""" src: https://serverfault.com/questions/1008556/is-there-a-need-for-the-nat-table-input-chain
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
""",back)])

def to_graph(_):
    
    ui_element.set_view(graph_view)
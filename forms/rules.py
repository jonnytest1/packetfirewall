from log import get_rules
from ui.baseelement import UITextElement
from ui.ui_textbutton_element import UITextButton

from forms.ui_ref import ui_element
from ui.ui_view import ui_view




def display_rules(_):
    

    rules=get_rules()

    rules_view=ui_view()
    rules_view.columns.append([UITextButton("back")])

    for rule in rules:
        chain=rule.propsdict["chain"]
        row:list[UITextElement] = [UITextButton(f"table:{rule.table}",rule.delete),UITextButton(f"chain:{chain.value}",rule.delete)]
        for key,val in rule.propsdict.items():
            if key!="chain":
                row.append(UITextButton(f"{key}:{val.value}",rule.delete))
        rules_view.columns.append(row)
    ui_element.set_view(rules_view)
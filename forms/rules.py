from log import get_rules
from ui.baseelement import UITextElement
from ui.ui_textbutton_element import UITextButton

from forms.ui_ref import ui_element

def display_rules(_):
    rules=get_rules()
    ui_element.set_columns([[UITextButton("back")]])

    for rule in rules:
        chain=rule.propsdict["chain"]
        row:list[UITextElement] = [UITextButton(f"table:{rule.table}"),UITextButton(f"chain:{chain.value}")]
        for key,val in rule.propsdict.items():
            if key!="chain":
                row.append(UITextButton(f"{key}:{val.value}",rule.delete))
        ui_element.columns.append(row)
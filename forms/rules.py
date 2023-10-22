
from ui.baseelement import UITextElement
from ui.ui_textbutton_element import UITextButton

from forms.ui_ref import ui_element
from ui.ui_view import ui_view
from tables_api import tables_api




def display_rules(_):
    

    rules=tables_api.get_rules()

    rules_view=ui_view()
    rules_view.columns.append([UITextButton("back")])

    for rule in rules:
        def delete_rule(_):
            tables_api.delete_rule(rule)

        chain=rule.propsdict["chain"]
        row:list[UITextElement] = [UITextButton(f"table:{rule.table}",delete_rule),UITextButton(f"chain:{chain.value}",delete_rule)]
        for key,val in rule.propsdict.items():
            if key!="chain":
                row.append(UITextButton(f"{key}:{val.value}",delete_rule))
        rules_view.columns.append(row)
    ui_element.set_view(rules_view)
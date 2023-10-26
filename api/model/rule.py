from api.model.rule_condition import Log_Rule_Condition



class IpTablesRule:
    
    def __init__(self,table:str):
        self.table=table
        self.propsdict:dict[str,Log_Rule_Condition]=dict()
        self.line:str
        self.mode:str

   


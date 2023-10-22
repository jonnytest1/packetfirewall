class Log_Rule_Condition:
    DESTINATION_PORT="dst_port"


    def __init__(self,type:str,value:str,negated:bool):
        self.type=type
        self.value=value
        self.negated=negated
    
    
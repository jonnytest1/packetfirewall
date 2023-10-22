from api.model.log_entry import LogEntry
from api.model.rule import IpTablesRule
from subprocess import run

from api.model.rule_condition import Log_Rule_Condition


tables=["filter","nat","mangle","raw","security"]

CONDITION_MAP={
        "-A" :"chain", #append to chain
        "-I" :"chain", #insert into chain
        "-N" :"chain", #new chain
        "-P" :"chain", #default policy for chain
        "-s" :"src_ip", #
        "-d" :"dst_ip", #
        "-m" :"match", #
        "-p" :"protocol", #
        "-i" :"in_interface", #
        "-o" :"out_interface", #

        "--dst-type" :"dst_type", # nat
        "--to-destination" :"nat_dst_ip", # nat
        "--dport" :"dst_port", # nat
        "--log-prefix" :"log_prefix", # log prefix
        "--ctstate" :"ctstate", #
        "-j" :"jump", #
}


INV_COND_MAP=dict()

for key,val in CONDITION_MAP.items():
    INV_COND_MAP[val]=key

class ip_tables:

    def ip_tables_rule_from_string(self,line:str,table:str):
        rule=IpTablesRule(table)
        words=line.split(" ")
        rule.line=line
        negated=False
        i=0
        while i<len(words):
            word=words[i]
            if word.startswith("-"):

                if(CONDITION_MAP[word] != None):
                    type_name=CONDITION_MAP[word]
                    next_word=words[i+1]
                    i=i+1
                    rule.propsdict[type_name]=Log_Rule_Condition(type_name,next_word,negated)
                else:
                    pass
                negated=False
            elif(word=="ACCEPT"):
                rule.mode="ACCEPT"
            elif(word=="DROP"):
                rule.mode="DROP"
            elif(word=="!"):
                negated=True
            else:
                pass

            i+=1

        return rule


    def condition_to_cmd(self,cond:Log_Rule_Condition):
        inversemapping=INV_COND_MAP[cond.type]

        if inversemapping == None:
            raise Exception("failed backwards mapping")
        negation=""
        if(cond.negated):
            negation="! "
        return f"{negation}{inversemapping} {cond.value}"

    def create_cmd(self,rule:IpTablesRule):
        conditions =""

        if "protocol" in rule.propsdict:
            cmd=self.condition_to_cmd(rule.propsdict["protocol"])
            # do protocol first since it needs to be before others
            conditions+=f"{cmd} "

        for key,val in rule.propsdict.items():
            if key !="chain" and key!="protocol":
                inversemapping=INV_COND_MAP[key]

                if inversemapping == None:
                    raise Exception("failed backwards mapping")
                conditions+=f"{inversemapping} {val.value} "

        chain=rule.propsdict["chain"].value
        fullcmd=f"iptables -t {rule.table} -A {chain} {conditions} "
        return fullcmd
    
    def delete_rule(self,rule:IpTablesRule):
    
        cmd=""
        for key,val in rule.propsdict.items():
            if key !="chain":
                inversemapping=INV_COND_MAP[key]

                if inversemapping == None:
                    raise Exception("failed backwards mapping")
                cmd+=f"{inversemapping} {val.value} "

        chain=rule.propsdict["chain"].value
        fullcmd=f"iptables -D {chain} -t {rule.table} {cmd}"
        runPr=run(fullcmd,shell=True,capture_output=True)
        successful=runPr.returncode
        if successful!=0:
            error=runPr.stderr
            raise Exception(error.decode())
        
    def get_rules(self):
        rules:list[IpTablesRule]=[]
        for table in tables:
            rule_std=run(f"iptables -S -t {table}",shell=True,capture_output=True)
            for rule in rule_std.stdout.decode().split("\n"):
                if(len(rule)):
                    rules.append(self.ip_tables_rule_from_string(rule,table))
        return rules


    def setup_logging(self,conditions:list[Log_Rule_Condition]):
        rules=self.get_rules()

        table_chains:dict[str,set[str]]=dict()

        for rule in rules:
            if rule.table not in table_chains:
                table_chains[rule.table]=set()
            table_chains[rule.table].add(rule.propsdict["chain"].value)
        condition_str=""

        for conditino in conditions:
            condition_str+= self.condition_to_cmd(conditino)+" "
        for table in tables:
            for chain in table_chains[table]:
                cmd=f"iptables -I {chain} -t {table} -j LOG --log-prefix 'LOG_INTERCEPT#{table}{chain}' {condition_str}"
                pr= run(cmd,shell=True,capture_output=True)
                output=pr.stdout.decode()
    
    def add_rule(self,params:IpTablesRule):
        create_cmd=self.create_cmd(params)
        create_output=run(create_cmd,shell=True,capture_output=True)
        create_output.check_returncode()

    def get_logs(self):
        pr= run("tail -n 1000 /var/log/kern.log",shell=True,capture_output=True)
        output=pr.stdout.decode()
        ar:list[LogEntry]=[]

        if(output is None):
            return ar

        for line in output.split("\n"):
            if(len(line)) and "LOG_INTERCEPT" in line:
                ar.append(LogEntry(line))
        return ar

        
    def cleanup_logging(self):
        rules=self.get_rules()
        for rule in rules:
            if "log_prefix" in rule.propsdict:
                if rule.propsdict["log_prefix"].value.startswith("\"LOG_INTERCEPT#"):
                    self.delete_rule(rule)
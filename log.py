
from subprocess import run
from re import search
from datetime import datetime


tables=["filter","nat","mangle","raw","security"]

class LogEntry:
    MATCHING_PROPS_FOR_GROUP=["dst_ip","src_ip","destination_port","protocol","interface_in","log_type"]

    def __init__(self,line:str):
        interface_match="IN=(?P<interface_in>[^ ]*?) OUT=(?P<interface_out>[^ ]*?) (PHYSIN=(?P<interfacephysin>[^ ]*?) )?"
        ip_match="SRC=(?P<src_ip>[^ ]*?) DST=(?P<dst_ip>[^ ]*?) "
        port_match="SPT=(?P<source_port>[^ ]*?) DPT=(?P<destination_port>[^ ]*?) "
        date_match="(?P<timestamp>.*?\\d\\d:\\d\\d:\\d\\d) (?P<pcname>.*?) kernel: \\[(?P<log_id_ct>.*?)\\] "

        match= search(f"{date_match}LOG_INTERCEPT#(?P<log_type>[^ ]*?){interface_match}MAC=(?P<mac>[^ ]*?) {ip_match}LEN=(?P<length>[^ ]*?) TOS=.*?ID=(?P<id>[^ ]*?) .*?PROTO=(?P<protocol>[^ ]*?) {port_match}",line)
        if match == None:
            return
        
        self.timestamp=match.group("timestamp")
        self.datetime=datetime.strptime(str(datetime.now().year)+" "+self.timestamp,"%Y %b %d %H:%M:%S")
        self.datetime.year
        self.log_type=match.group("log_type")
        self.interface_in=match.group("interface_in")
        self.interface_out=match.group("interface_out")
        self.interface_in_phys=match.group("interfacephysin")
        self.mac_address=match.group("mac")
        self.protocol=match.group("protocol")
        self.src_ip=match.group("src_ip")
        self.dst_ip=match.group("dst_ip")
        self.source_port=match.group("source_port")
        self.destination_port=match.group("destination_port")
        self.id=match.group("id")


        self.prop_dict=match.groupdict()
    
    def grouped(self,other:"LogEntry"):
        for prop in LogEntry.MATCHING_PROPS_FOR_GROUP:
            if other.prop_dict[prop] != self.prop_dict[prop]:
                return False

        return True


class Condition:
    def __init__(self,type:str,value:str,negated:bool):
        self.type=type
        self.value=value
        self.negated=negated
    
    def to_cmd(self):
        inversemapping=INV_COND_MAP[self.type]

        if inversemapping == None:
            raise Exception("failed backwards mapping")
        negation=""
        if(self.negated):
            negation="! "
        return f"{negation}{inversemapping} {self.value}"


class IpTablesRule:

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
        "--to-destination" :"dst_ip", # nat
        "--dport" :"dst_port", # nat
        "--log-prefix" :"log_prefix", # log prefix
        "--ctstate" :"ctstate", #
        "-j" :"jump", #

    }


    def __init__(self,line:str,table:str):
        self.table=table

        words=line.split(" ")
        self.line=line
        self.propsdict:dict[str,Condition]=dict()
        negated=False
        i=0
        while i<len(words):
            word=words[i]
            if word.startswith("-"):

                if(IpTablesRule.CONDITION_MAP[word] != None):
                    type_name=IpTablesRule.CONDITION_MAP[word]
                    next_word=words[i+1]
                    i=i+1
                    self.propsdict[type_name]=Condition(type_name,next_word,negated)
                else:
                    pass
                negated=False
            elif(word=="ACCEPT"):
                self.mode="ACCEPT"
            elif(word=="DROP"):
                self.mode="DROP"
            elif(word=="!"):
                negated=True
            else:
                pass

            i+=1

    def delete(self):

        cmd=""
        for key,val in self.propsdict.items():
            if key !="chain":
                inversemapping=INV_COND_MAP[key]

                if inversemapping == None:
                    raise Exception("failed backwards mapping")
                cmd+=f"{inversemapping} {val.value} "

        chain=self.propsdict["chain"].value
        fullcmd=f"iptables -D {chain} -t {self.table} {cmd}"
        runPr=run(fullcmd,shell=True,capture_output=True)
        successful=runPr.returncode
        if successful!=0:
            error=runPr.stderr
            raise Exception(error.decode())
        pass



   # run("echo \":msg,contains,\"[LOG_INTERCEPT]\" /var/log/iptables.log\" >> " ,shell=True,capture_output=True)
    #run("systemctl restart rsyslog" ,shell=True,capture_output=True)
    #run("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True,capture_output=True)

def setup_logging(conditions:list[Condition]):
    rules=get_rules()

    table_chains:dict[str,set[str]]=dict()

    for rule in rules:
        if rule.table not in table_chains:
            table_chains[rule.table]=set()
        table_chains[rule.table].add(rule.propsdict["chain"].value)
    condition_str=""

    for conditino in conditions:
        condition_str+= conditino.to_cmd()+" "
    for table in tables:
        for chain in table_chains[table]:
            cmd=f"iptables -I {chain} -t {table} -j LOG --log-prefix 'LOG_INTERCEPT#{table}{chain}' {condition_str}"
            pr= run(cmd,shell=True,capture_output=True)
            output=pr.stdout.decode()

def cleanup_logging():
    rules=get_rules()
    for rule in rules:
        if "log_prefix" in rule.propsdict:
            if rule.propsdict["log_prefix"].value.startswith("\"LOG_INTERCEPT#"):
                rule.delete()


def get_logs():
    pr= run("tail -n 1000 /var/log/kern.log",shell=True,capture_output=True)
    output=pr.stdout.decode()
    ar:list[LogEntry]=[]

    if(output is None):
        return ar

    for line in output.split("\n"):
        if(len(line)):
            ar.append(LogEntry(line))
    return ar


def get_rules():

    rules:list[IpTablesRule]=[]
    for table in tables:
        rule_std=run(f"iptables -S -t {table}",shell=True,capture_output=True)
        for rule in rule_std.stdout.decode().split("\n"):
            if(len(rule)):
                rules.append(IpTablesRule(rule,table))
    return rules

        


INV_COND_MAP=dict()

for key,val in IpTablesRule.CONDITION_MAP.items():
    INV_COND_MAP[val]=key
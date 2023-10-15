from os import system
from subprocess import run
from re import search

tables=["filter","nat","mangle","raw","security"]

"""Oct 15 00:00:29 PCn kernel: [21219.536922] LOG_INTERCEPT#INPUTIN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 SRC=127.0.0.1 DST=127.0.0.1 LEN=109 TOS=0x00 PREC=0x00 TTL=64 ID=46133 DF PROTO=TCP SPT=52050 DPT=34249 WINDOW=24571 RES=0x00 ACK PSH URGP=0 """
class LogEntry:
    def __init__(self,line:str):
        interface_match="IN=(?P<interfacein>[^ ]*?) OUT=(?P<interfaceout>[^ ]*?) (PHYSIN=(?P<interfacephysin>[^ ]*?) )?"
        ip_match="SRC=(?P<src_ip>[^ ]*?) DST=(?P<dst_ip>[^ ]*?) "
        port_match="SPT=(?P<source_port>[^ ]*?) DPT=(?P<destination_port>[^ ]*?) "
        match= search(f"LOG_INTERCEPT#(?P<type>[^ ]*?){interface_match}MAC=(?P<mac>[^ ]*?) {ip_match}LEN=(?P<length>[^ ]*?) TOS=.*?ID=(?P<id>[^ ]*?) .*?PROTO=(?P<protocol>[^ ]*?) {port_match}",line)
        if match == None:
            return
        
        self.log_type=match.group("type")
        self.interface_in=match.group("interfacein")
        self.interface_out=match.group("interfaceout")
        self.interface_in_phys=match.group("interfacephysin")
        self.mac_address=match.group("mac")
        self.protocol=match.group("protocol")
        self.src_ip=match.group("src_ip")
        self.dst_ip=match.group("dst_ip")
        self.source_port=match.group("source_port")
        self.destination_port=match.group("destination_port")
        self.id=match.group("id")
    
    def grouped(self,other:"LogEntry"):
        return other.dst_ip==self.dst_ip and other.destination_port==self.destination_port and other.protocol == self.protocol and other.interface_in == self.interface_in and other.log_type==self.log_type and other.src_ip==self.src_ip


class Condition:
    def __init__(self,type:str,value:str,negated:bool):
        self.type=type
        self.value=value
        self.negated=negated

class IpTablesRule:
    def __init__(self,line:str,table:str):
        self.table=table

        words=line.split(" ")

        self.conditions:list[Condition]=[]
        negated=False
        i=0
        while i<len(words):
            word=words[i]
            if word.startswith("-"):
                
                if(word=="-A" or word =="-I"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("step",next_word,negated))
                elif(word=="-N"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("new_chain",next_word,negated))
                elif(word=="-P"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("policy",next_word,negated))
                elif(word=="-s"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("src_ip",next_word,negated))
                elif(word=="-d"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("dst_ip",next_word,negated))
                elif(word=="-m"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("match",next_word,negated))
                elif(word=="-p"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("protocol",next_word,negated))
                elif(word=="-i"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("in_interface",next_word,negated))
                elif(word=="-o"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("out_interface",next_word,negated))
                elif(word=="--dst-type"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("dst-type",next_word,negated))
                elif(word=="--to-destination"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("dst-ip",next_word,negated))
                elif(word=="--log-prefix"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("log-prefix",next_word,negated))
                elif(word=="--dport"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("dst-port",next_word,negated))
                elif(word=="--ctstate"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("ctstate",next_word,negated))
                elif(word=="-j"):
                    next_word=words[i+1]
                    i=i+1
                    self.conditions.append(Condition("jump",next_word,negated))
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



def setupLogging():
    system("echo \":msg,contains,\"[LOG_INTERCEPT]\" /var/log/iptables.log\" >> " )
    system("systemctl restart rsyslog" )
    system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def registerLogging():
    system("iptables -I INPUT -j LOG --log-prefix 'LOG_INTERCEPT#INPUT'")



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

    rules=[]
    for table in tables:
        rule_std=run(f"iptables -S -t {table}",shell=True,capture_output=True)
        for rule in rule_std.stdout.decode().split("\n"):
            if(len(rule)):
                rules.append(IpTablesRule(rule,table))
    return rules

        
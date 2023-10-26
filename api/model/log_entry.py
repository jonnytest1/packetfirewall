from re import search
from datetime import datetime


class LogEntry:
    MATCHING_PROPS_FOR_GROUP=["dst_ip","src_ip","destination_port","protocol","interface_in"] #,"log_type"

    def __init__(self,line:str):
        interface_match="IN=(?P<interface_in>[^ ]*?) OUT=(?P<interface_out>[^ ]*?) (PHYSIN=(?P<interfacephysin>[^ ]*?) )?"
        ip_match="SRC=(?P<src_ip>[^ ]*?) DST=(?P<dst_ip>[^ ]*?) "
        port_match="SPT=(?P<source_port>[^ ]*?) DPT=(?P<destination_port>[^ ]*?) "
        date_match="(?P<timestamp>.*?\\d\\d:\\d\\d:\\d\\d) (?P<pcname>.*?) kernel: (\\[(?P<log_id_ct>.*?)\\] )?"

        match= search(f"{date_match}(?P<log_type>LOG_INTERCEPT#[^ ]*?){interface_match}(MAC=(?P<mac>[^ ]*?) )?{ip_match}LEN=(?P<length>[^ ]*?) TOS=.*?ID=(?P<id>[^ ]*?) .*?PROTO=(?P<protocol>[^ ]*?) {port_match}",line)
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


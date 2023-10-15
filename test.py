import datetime
from log import LogEntry, get_rules


line="Oct 15 00:42:03 PCn kernel: [23713.383104] LOG_INTERCEPT#INPUTIN=br-48bfeaaccb0a OUT= PHYSIN=vetha6d49a3 MAC=02:42:4d:24:86:4d:02:42:ac:12:00:02:08:00 SRC=172.18.0.2 DST=172.18.0.1 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=9000 DPT=51114 WINDOW=65160 RES=0x00 ACK SYN URGP=0 "

log=LogEntry(line)

testdate="Oct 15 17:17:18"

time=datetime.datetime.strptime(testdate,"%b %d %H:%M:%S")




assert True
import datetime
from log import LogEntry, get_rules

testdate="Oct 15 17:17:18"

time=datetime.datetime.strptime(testdate,"%b %d %H:%M:%S")

assert True
import datetime

from api.nftables import nf_tables

testdate="Oct 15 17:17:18"

time=datetime.datetime.strptime(testdate,"%b %d %H:%M:%S")

rules=nf_tables().get_rules()


assert True
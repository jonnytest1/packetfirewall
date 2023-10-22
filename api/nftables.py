from subprocess import run
from json import loads,dumps

from api.model.rule import IpTablesRule
class nf_tables:

    #TODO: get_rules seems to remove dnat options (and others) when formatted as json

    def get_rules(self):
        pr=run("nft -j list ruleset",shell=True,capture_output=True)
        pr.check_returncode()
        rules=loads(pr.stdout)
        rule_list:list[IpTablesRule]

        for rule in rules["nftables"]:
            if "rule" in rule:
                ruleObj=IpTablesRule(rule["rule"]["table"])
                ruleObj.line=dumps(rule)
                ruleObj.mode=rule["rule"]["policy"]

        pass


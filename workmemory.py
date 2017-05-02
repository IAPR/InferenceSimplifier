from statement import Statement
from symbol import *

from copy import deepcopy

class WorkMemory:
    """Maintains rules for the inference engine in memory"""
    def __init__(self):
        # Rules:
        #   - Identifier
        #   - Value
        self.rules = {}

    def __str__(self):
        rstr = ""
        for rule,val in self.rules.items():
            rstr += str(rule) + " = " + str(val) + "\n"
        return rstr

    def copy(self):
        """Makes a full copy of the rule"""
        return deepcopy(self)

    def RuleExists(self, st_str):
        """Checks if a rule already exists"""
        if( self.rules.get(st_str) is None):
            return False
        else:
            return True

    def AddRule(self, statement, value):
        """Adds a rule of identifier=value"""
        st_str = str(statement)

        # Fail if rule already exists
        if(self.RuleExists(st_str)):
            print("Rule {0} already exists, with value {1}".format(statement, value))
            raise ValueError

        self.rules[st_str] = value

        print("NEW RULE ADDED")
        print(statement, "=", value)

    def GetRule(self, statement):
        st_str = str(statement)

        # Gets value of rule, else it fails
        for rule in self.rules.keys():
            if(rule == st_str):
                return self.rules[rule]
        return None

    def GetPastKeys(self, statement):
        """Finds all keys before the one searched"""
        st_str = str(statement)
        keys = []
        for rule in self.rules.keys():
            if(rule != st_str):
                keys.append(rule)
            else:
                return keys
        return None


    def ModifyRule(self, statement, value):
        """Modifies an existing rule"""
        st_str = str(statement)

        # Fail if rule already exists
        if(not self.RuleExists(st_str)):
            raise ValueError

        self.rules[st_str] = value

        print("RULE MODIFIED")
        print(statement, "=", value)

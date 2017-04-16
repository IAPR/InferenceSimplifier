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
            raise ValueError

        self.rules[st_str] = value

        print("NEW RULE ADDED")
        print(statement, "=", value)

    def ModifyRule(self, statement, value):
        """Modifies an existing rule"""
        st_str = str(statement)

        # Fail if rule already exists
        if(not self.RuleExists(st_str)):
            raise ValueError

        self.rules[st_str] = value

        print("RULE MODIFIED")
        print(statement, "=", value)

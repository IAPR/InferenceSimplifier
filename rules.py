from statement import Statement
from symbol import *

from copy import deepcopy
import os
import json

class Rules:
    """Contains a list of CNF statements that will later be used"""
    def __init__(self, f_name):
        self.rules = []
        self.file = f_name
        if(os.path.exists(self.file)):
            self.Load()

    def __str__(self):
        rstr = ""
        for rule in self.rules:
            rstr += str(rule) + "\n"
        return rstr

    def copy(self):
        """Makes a full copy of the list of rules"""
        return deepcopy(self)

    def RuleExists(self, st_str):
        """Check if a statement exists"""
        if( st_str in self.rules):
            return True
        else:
            return False

    def CreateRule(self, statement):
        """Creates a new Rule from an existing statement"""
        st_str = str(statement)

        # Fail if rule already exists
        if(self.RuleExists(st_str)):
            raise ValueError

        self.rules.append(st_str)

        print("NEW RULE ADDED")
        print(statement)

    def Load(self):
        """Loads from an existing file"""
        fp = open(self.file, "r")
        rules = fp.read()
        self.rules = json.loads(rules)

    def Save(self):
        """Saves to the file described in self.file"""
        rules_s = json.dumps(self.rules)
        fp = open(self.file, "w")
        fp.write(rules_s)
        fp.close()

    def GetSolutions(self):
        """Check for a ruleset that became a solution through Modus Tollens"""
        #
        # A rule is a solution if there is only one variable left in the rule
        #
        solutions = []
        for con,ants in self.rules.items():
            for ant in ants:
                if(ant.strip() in ["F", "T"]):
                    solutions.append( str(ant) + " -> " + str(con) )
        return solutions

    def Propagate(self, item, value):
        """Replaces a variable with a specific value, either T or F"""
        if(item == ""):
            return
        # Only valid values are our True of False (T,F)
        value = value.strip()
        if(value not in ["T", "F"]):
            raise ValueError

        print("Rules before propagation")
        print(self)

        for rule in self.rules:
            rule_st = Statement(rule)
            rule_st.ReplaceWithValue(item,value)

        print("Rules after propagation")
        print(self)

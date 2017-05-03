from statement import Statement
from symbol import *

from copy import deepcopy
import os
import json

class WorkMemory:
    """Maintains rules for the inference engine in memory"""
    def __init__(self, f_name=""):
        # Rules:
        #   - Identifier
        #   - Value
        self.rules = {}
        self.file = f_name
        if(os.path.exists(self.file)):
            self.Load()

    def __str__(self):
        rstr = ""
        for rule,val in self.rules.items():
            rstr += str(rule) + " = " + str(val) + "\n"
        return rstr

    def copy(self):
        """Makes a full copy of the rule"""
        return deepcopy(self)

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

    def RuleExists(self, st_str):
        """Checks if a rule already exists"""
        if( self.rules.get(st_str) is None):
            return False
        else:
            return True

    def AddRule(self, statement, value):
        """Adds a rule of identifier->value, or consequent->antecedent"""
        st_str = str(statement)
        val_str = str(value)

        # Fail if rule already exists
        if(self.RuleExists(st_str)):
            print("Rule {0} already xists, with value {1}".format(statement, val_str))
            raise ValueError

        self.rules[st_str] = val_str

        print("NEW RULE ADDED")
        print(statement, "=", val_str)

    def RemoveRule(self, statement):
        """Removes an existent rule"""
        st_str = str(statement)

        # Pops rule
        if(self.RuleExists(st_str)):
            self.rules.pop(st_str)
        else:
            raise IndexError

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
        val_str = str(value)

        # Fail if rule already exists
        if(not self.RuleExists(st_str)):
            raise ValueError

        self.rules[st_str] = val_str

        print("RULE MODIFIED")
        print(statement, "=", val_str)

    def GetSolutions(self):
        """Check for a ruleset that became a solution through Modus Ponens"""
        solutions = []
        for con,ants in self.rules.items():
            for ant in ants:
                if(ant.strip() in ["F", "T"]):
                    solutions.append( str(ant) + " -> " + str(con) )
        return solutions

    def IsSolved(self):
        undef = self.GetSolutions()
        return len(undef) == len(self.rules)

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

        for con,ant in self.rules.items():
            # If propagation extends to a consequent, modify that rule
            if( str(con).strip() == item):
                self.ModifyRule(con, value)
                continue

            ant = Antecedent(ant_str)
            changed = ant.root.ReplaceInTree(item, value)

        #i = 0
        #while(i < len(self.rules)):
        #    rule_st = Statement(self.rules[i])
        #    rule_st.ReplaceWithValue(item,value)
        #    self.rules[i] = str(rule_st)
        #    i += 1;

        print("Rules after propagation")
        print(self)

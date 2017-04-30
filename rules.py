from statement import Statement
from symbol import *

from copy import deepcopy
import os
import json
import re

class Rules:
    """Contains a list of CNF statements that will later be used"""
    def __init__(self, f_name=""):
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
        regex = "^[\w]+$"
        solutions = []
        for rule in self.rules:
            rule_st = Statement(rule)
            if(rule_st.root.symbol.code == "IDENTIFIER"): 
                if(rule_st.root.symbol.mask not in ["T", "F"]):
                    solutions.append(rule)
        return solutions

    def IsSolved(self):
        solutions = self.GetSolutions()
        if( len(solutions) == len(self.rules) ):
            print("SOLUTIONS", solutions)
            print("RULES====", self.rules) 
            return True
        else:
            return False

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

        i = 0
        while(i < len(self.rules)):
            rule_st = Statement(self.rules[i])
            rule_st.ReplaceWithValue(item,value)
            self.rules[i] = str(rule_st)
            i += 1;

        print("Rules after propagation")
        print(self)

    def GetIdentifiers(self):
        id_regex = "\w+"
        ids = []
        for rule in self.rules:
            id_lst = re.findall(id_regex, rule)
            for iD in id_lst:
                if("v" not in iD):
                    ids.append(iD)
        ids = list(set(ids))
        return ids

    def GetRelatedRules(self, identifier):
        id_queue = [identifier]
        id_cons = []
        id_ants = []
        rules_lst = []

        while(len(id_queue) > 0):
            has_related_rules = False
            qid = id_queue[0]
            # Check in which rules the id appears
            for rule in self.rules:
                # If found in rule, add it to the list
                if(qid in rule and rule not in rules_lst):
                    rules_lst.append(rule)
                    has_related_rules = True
            if(has_related_rules):
                if(qid not in id_cons):
                    id_cons.append(qid)
            else:
                if(qid not in id_ants):
                    id_ants.append(qid)
            # Eliminate id from queue
            id_queue.pop(0)
            # Get all the new Identifiers from the new rules
            tmp = Rules()
            for rule in rules_lst:
                tmp.CreateRule(rule)
            new_id_list = tmp.GetIdentifiers()
            for nid in new_id_list:
                if(nid not in id_cons and nid not in id_ants):
                    id_queue.append(nid)

        return {"CONS": id_cons, "ANTS": id_ants, "RULES": rules_lst }

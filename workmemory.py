from statement import Statement
from symbol import *

from copy import deepcopy
import os
import json
import re

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
        for rule,val_list in self.rules.items():
            for val in val_list:
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

    def ListIdentifiers(self):
        return self.ListConsequents() + self.ListAntecedents()

    def ListConsequents(self):
        """Get a list of all consequents in the memory"""
        return list(self.rules.keys())

    def ListAntecedents(self):
        """Get a list of all antecedents in memory"""
        id_regex = "\w+"
        ids = []
        for con, ant_lst in self.rules.items():
            for ant in ant_lst:
                id_lst = re.findall(id_regex, ant)
                for iD in id_lst:
                    if("v" in iD):
                        continue    
                    elif(iD in ["T", "F"]):
                        continue
                    ids.append(iD)
        ids = list(set(ids))
        return ids 

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
            self.rules[st_str].append(val_str)
        else:
            self.rules[st_str] = [val_str]

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

    def GetRules(self, statement):
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

    def GetSolutions(self):
        """Check for a ruleset that became a solution through Modus Ponens"""
        solutions = []
        for con,ants in self.rules.items():
            for ant in ants:
                if(ant.strip() in ["F", "T"]):
                    solutions.append( str(con) + "=" + str(ant) )
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

        for con,ant_lst in self.rules.items():
            # If propagation extends to a consequent, modify that rule
            if( str(con).strip() == item):
                self.RemoveRule(con)
                self.AddRule(con, value)
                continue

            # Propagate to each of the rules for each consequent
            new_rules = []
            for ant_str in ant_lst:
                ant = Statement(ant_str)
                ant.ReplaceWithValue(item, value)
                new_rules.append( str(ant) )

            # Place the new heap of rules
            self.RemoveRule(con)
            for nrule in new_rules:
                self.AddRule(con, nrule)

        print("Rules after propagation")
        print(self)

    def GetRelatedRules(self, identifier):
        id_queue = [identifier]
        id_checked = []
        rules_lst = {}

        while(len(id_queue) > 0):
            print("IDQUEUE", id_queue)
            print("CHECKED", id_checked)
            print("RULES", rules_lst)

            qid = id_queue[0]
            # Check in which rules the id appears
            for con,ant_lst in self.rules.items():
                for ant in ant_lst:
                    # If found in rule, add it to the dictionary
                    if(qid in ant or qid in con):
                        if(rules_lst.get(con) is None):
                            rules_lst[con] = [ant]
                        else:
                            rules_lst[con].append(ant)
                        rules_lst[con] = list( set( rules_lst[con] ) )
            # Eliminate id from queue
            id_queue.pop(0)
            id_checked.append(qid)
            # Get all the new Identifiers from the new rules
            tmp = WorkMemory()
            for con,ant_lst in rules_lst.items():
                for ant in ant_lst:
                    tmp.AddRule(con, ant)
            new_id_list = tmp.ListIdentifiers()
            # Queue all identifiers that has not been checked already
            for nid in new_id_list:
                if(nid not in id_checked):
                    id_queue.append(nid)

        # Generate a new workmemory object for storing the new rules
        print("RULES:", rules_lst)
        newMem = WorkMemory()
        for con, ant_lst in rules_lst.items():
            for ant in ant_lst:
                newMem.AddRule(con, ant)
        return newMem


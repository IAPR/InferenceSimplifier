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
        solutions = []
        for con,ants in self.rules.items():
            for ant in ants:
                if(ant.strip() in ["F", "T"]):
                    solutions.append( str(ant) + " -> " + str(con) )
        return solutions

    def Propagate(self, item, value):
        if(item == ""):
            return
        if(value):
            val = "T"
        else:
            val = "F"

        print("Rules before propagation")
        print(self)

        for con,ants in self.rules.items():
            # If a given value is given, everything is restarted
#            if( str(con).strip() == item):
#                ants.clear()
#                ants.append(val)
#                continue

            for ant_str in ants:
                ant = Antecedent(ant_str)
                changed = ant.root.ReplaceInTree(item, value)
                ant.SimplifyToMinimum()
                ants.pop( ants.index(ant_str) )
                ants.append( str(ant) )
                if(changed and str(ant).strip() in ["F", "T"]):
                    self.Propagate(con, str(ant).strip() )

        print("Rules after propagation")
        print(self)

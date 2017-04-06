from antecedent import Antecedent
from consequent import Consequent
from statement import Statement
from symbol import *

import os
import json

class WorkMemory:
    def __init__(self, f_name):
        # Rules:
        #   - Identifier
        #   - List of antecedents
        self.rules = {}
        self.file = f_name
#        if(os.path.exists(self.file)):
#            self.Load()

    def __str__(self):
        rstr = ""
        for con, ants in self.rules.items():
            for ant in ants:
                rstr += ant + " -> " + con + "\n"
        return rstr

    def AddRule(self, rule):
        ant_str = str(rule.antecedent).strip()
        con_str = str(rule.consequent).strip()
        # Add antecedent to the list of the corresponding consequent
        if(self.rules.get(con_str) == None):
            self.rules[con_str] = [ant_str]
        else:
            self.rules[con_str].append(ant_str)

        print("NEW RULE DETECTED")
        print("Antecedent string: ", ant_str)
        print(Antecedent(ant_str))
        print("Consequent string: ", con_str)
        print(Consequent(con_str))

    def Load(self):
        fp = open(self.file, "r")
        work_mem_s = fp.read()
        self.__dict__ = json.loads(work_mem_s)

    def Save(self):
        work_mem_s = json.dumps(self.__dict__)
        fp = open(self.file, "w")
        fp.write(work_mem_s)
        fp.close()

    def GetSolutions(self):
        solutions = []
        for con,ants in self.rules:
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

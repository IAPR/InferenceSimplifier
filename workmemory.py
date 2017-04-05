from antecedent import Antecedent
from consequent import Consequent
from statement import Statement
from symbol import *

import os
import json

class WorkMemory:
    def __init__(self, f_name):
        self.rules = {}
        self.file = f_name
        if(os.path.exists(self.file)):
            self.Load()

    def AddRule(self, rule):
        ant_str = str(rule.antecedent).strip()
        con_str = str(rule.consequent).strip()
        self.rules[con_str] = ant_str

        print("NEW RULE DETECTED")
        print("Antecedent string: ", ant_str)
        print(Antecedent(ant_str))
        print("Consequent string: ", con_str)
        print(Consequent(con_str))
        input()

    def Load(self):
        fp = open(self.file, "r")
        work_mem_s = fp.read()
        self.__dict__ = json.loads(work_mem_s)

    def Save(self):
        work_mem_s = json.dumps(self.__dict__)
        fp = open(self.file, "w")
        fp.write(work_mem_s)
        fp.close()

    def Propagate(self, item, value):
        if(item == ""):
            return
        if(value):
            val = "T"
        else:
            val = "F"

        for con in self.rules.keys():
            ant = Antecedent(self.rules[con])
            print("BEFORE PROPAGATION", ant)
            print(repr(ant))
            input("Press Enter")
            ant.root.ReplaceInTree(item, value)
            print("AFTER PROPAGATION", ant)
            print(repr(ant))
            input("Press Enter")
            self.rules[con] = str(ant)
            print(self.rules[con], "->", con)

        print("RULES")
        for con,ant in self.rules.items():
            print(ant, "->", con)

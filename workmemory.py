from antecedent import Antecedent
from consequent import Consequent
from statement import Statement
from symbol import *

import os
import json

class WorkMemory:
    def __init__(self, f_name):
        self.rules = []
        self.file = f_name
        if(os.path.exists(self.file)):
            self.Load()

    def AddRule(self, rule):
        self.rules.append(rule)

    def Load(self):
        fp = open(self.file, "r")
        work_mem_s = fp.read()
        self.__dict__ = json.loads(work_mem_s)

    def Save(self):
        work_mem_s = json.dumps(self.__dict__)
        fp = open(self.file, "w")
        fp.write(work_mem_s)
        fp.close()

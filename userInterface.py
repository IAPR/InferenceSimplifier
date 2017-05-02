from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from rules import Rules
from statement import Statement
from workmemory import WorkMemory

class ObjectiveWidget(QWidget):
    """Dialog/Widget for asking the objective of the reasoning"""
    def __init__(self, parent=None):
        super(ObjectiveWidget, self).__init__(parent)
        self.memRules = Rules("rulelist.json")
        self.id_lst = self.memRules.GetIdentifiers()

        self.lbl = QLabel("Specify your objective:")

        self.id_cmb = QComboBox()
        for id_item in self.id_lst:
            self.id_cmb.addItem(id_item)
        
        self.accept_btn = QPushButton("Accept")
        self.accept_btn.clicked.connect(self.SelectObjective)

        self.quest_layout = QHBoxLayout()
        self.quest_layout.addWidget(self.lbl)
        self.quest_layout.addWidget(self.id_cmb)
        self.quest_layout.addWidget(self.accept_btn)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.quest_layout)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Objective Reasoning")

    def SelectObjective(self):
        self.objective = self.id_cmb.currentText().strip()
        direct = QuestionWidget(self.objective, self)
        self.main_layout.addWidget(direct)

class QuestionWidget(QWidget):
    """Widget for creating and answering the questions that are needed in the reasoning"""
    def __init__(self, objective, parent = None):
        super(QuestionWidget, self).__init__(parent)
        self.objective = objective
        self.memRules = Rules("rulelist.json")
        self.reasoned = []

        # Get consequents, antecedents and list of rules pertaining the objective
        related = self.memRules.GetRelatedRules(self.objective)
        self.cons = related["CONS"]
        self.ants = related["ANTS"]

        # Generate question list
        self.question_list = []
        for con in self.cons[1:]:
            self.question_list.append(con)
        for ant in self.ants:
            self.question_list.append(ant)
        self.question = ""

        self.ruleHeap = Rules()
        for rule in related["RULES"]:
            self.ruleHeap.CreateRule(rule)

        # Value log will be a workmemory object
        self.valueLog = WorkMemory()
        
        self.lbl = QLabel('Especifique el valor de "<ID>":')
        
        self.value_edit = QComboBox()
        self.value_edit.addItem("T")
        self.value_edit.addItem("F")

        self.replace_btn = QPushButton("Replace")
        self.replace_btn.clicked.connect(self.Replace)
        
        self.rules_heap = QPlainTextEdit()
        self.rules_heap.setReadOnly(True)
        self.value_logs = QPlainTextEdit()
        self.value_logs.setReadOnly(True)

        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.lbl)
        self.hlayout1.addWidget(self.value_edit)
        self.hlayout1.addWidget(self.replace_btn)

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.rules_heap)
        self.hlayout2.addWidget(self.value_logs)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.hlayout1)
        self.main_layout.addLayout(self.hlayout2)

        self.UpdateValueLog()
        self.UpdateRuleHeap()
        self.SetNextQuestion()

        self.setLayout(self.main_layout)
        self.setWindowTitle("Objective Reasoning - Questioning")
        self.show()

    def SetNextQuestion(self):
        idList = self.ruleHeap.GetIdentifiers()

        self.question = ""
        while(self.question not in idList):
            self.question = self.question_list.pop()
            print("IDLIST", idList)
            print("Selected {0} for question".format(self.question))
            if(self.question not in idList):
                msg = QMessageBox()
                msg.setText("SKIP")
                msg.exec()

        self.lbl.setText('Especifique el valor de "{0}":'.format(self.question))
        self.UpdateValueLog()
        self.UpdateRuleHeap()
        
    def Replace(self):
        # Get the rule
        value = self.value_edit.currentText().strip()
        # Add it to the logs
        self.valueLog.AddRule(self.question, value)
        # Propagate rule
        self.ruleHeap.Propagate(self.question, value)
        # If solutions are found, add them to logs and propagate them
        solutions = self.ruleHeap.GetSolutions()
        for sol in solutions:
            sol_st = Statement(sol)
            if(sol_st.root.sign):
                val = "T"
            else:
                val = "F"
            if(sol_st.root.symbol.mask not in ["T", "F"]):
                self.valueLog.AddRule(sol_st.root.symbol.mask, val)
                self.ruleHeap.Propagate(sol_st.root.symbol.mask, val)
                self.reasoned.append(sol_st.root.symbol.mask)

        self.UpdateValueLog()
        self.UpdateRuleHeap()
        if(self.ruleHeap.IsSolved()):
            # Enter finished state
            if(self.valueLog.RuleExists(self.objective)):
                self.Explain()
            else:
                self.Fail()
        else:
            try:
                self.SetNextQuestion()
            except:
                self.Fail()

    def UpdateValueLog(self):
        self.value_logs.setPlainText( str(self.valueLog) + 
                "\n\nCONS: " + str(self.cons) + 
                "\n\nANTS: " + str(self.ants) +
                "\n\nQUESTIONS: " + str(self.question_list) +
                "\n\nQUESTION: " + str(self.question) + 
                "\n\nOBJECTIVE: " + str(self.objective) )

    def UpdateRuleHeap(self):
        self.rules_heap.setPlainText( str(self.ruleHeap) )

    def Finish(self):
        self.id_cmb.setReadOnly(True)
        self.replace_btn.setEnabled(False)


    def Fail(self):
        message = QMessageBox()
        message.setText("I couldn't find a solution for this problem.Reasoning tree was exhausted before an answer was found")
        message.exec()

    def Explain(self):
        explain_str = "Solution has been found: {0}\n".format(self.valueLog.GetRule(self.objective))
        for re in self.reasoned:
            past_lst = self.valueLog.GetPastKeys(re)
            explain_str += "\n{0} is {1} because:\n".format(re, self.valueLog.GetRule(re))
            for p in past_lst:
                explain_str += "\t{0} = {1}\n".format(p, self.valueLog.GetRule(p))
        msg = QMessageBox()
        msg.setText(explain_str)
        msg.exec()
            



from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from statement import Statement
from workmemory import WorkMemory

class ObjectiveWidget(QWidget):
    """Dialog/Widget for asking the objective of the reasoning"""
    def __init__(self, parent=None):
        super(ObjectiveWidget, self).__init__(parent)
        self.memRules = WorkMemory("rulelist.json")
        self.id_lst = self.memRules.ListConsequents()

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
        self.setWindowTitle("Backward Chaining Reasoning")

    def SelectObjective(self):
        self.objective = self.id_cmb.currentText().strip()
        direct = QuestionWidget(self.objective, self)
        self.main_layout.addWidget(direct)

class QuestionWidget(QWidget):
    """Widget for creating and answering the questions that are needed in the reasoning"""
    def __init__(self, objective, parent = None):
        super(QuestionWidget, self).__init__(parent)
        self.objective = objective
        self.memRules = WorkMemory("rulelist.json")
        self.reasoned = []

        # Create buffer of rules
        self.ruleHeap = self.memRules.copy()
        self.ruleHeap.file = ""

        # Generate question list
        self.question_list = self.ruleHeap.ListAntecedents()
        self.question = ""

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
        idList = self.ruleHeap.ListAntecedents()

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
            # Solution format "con=ant"
            con,ant = sol.split("=")

            # If rule has not been found before, propagate
            if( (not self.valueLog.RuleExists(con)) ):
                msg = QMessageBox()
                msg.setText("Discovered new rule: " + str(con) + " = " + str(ant) )
                msg.exec()

                self.valueLog.AddRule(con, ant)
                self.ruleHeap.Propagate(con, ant)
                self.reasoned.append(con)
            # If rule has already been found, check for inconsistencies
            elif( not self.valueLog.GetRules(con)[0] == ant):
                msg = QMessageBox()
                msg.setText("Inconsistency has been found: " + con + " was " + 
                        self.valueLog.GetRules(con)[0] + " but now it is " + ant)
                msg.exec()



        self.UpdateValueLog()
        self.UpdateRuleHeap()
        if(self.ruleHeap.IsSolved() or self.valueLog.RuleExists(self.objective)):
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
        final_value = self.valueLog.GetRules(self.objective)[0]
        explain_str = "Solution has been found: {0}\n".format(final_value)
        for re in self.reasoned:
            past_lst = self.valueLog.GetPastKeys(re)
            explain_str += "\n{0} is {1} because:\n".format(re, self.valueLog.GetRules(re)[0])
            for p in past_lst:
                rules = self.valueLog.GetRules(p)
                for rule in rules:
                    explain_str += "\t{0} = {1}\n".format(p, rule)
        msg = QMessageBox()
        msg.setText(explain_str)
        msg.exec()
            



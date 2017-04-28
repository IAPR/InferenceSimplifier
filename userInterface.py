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

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.quest_layout)
        self.main_layout.addWidget(self.accept_btn)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Objective Reasoning")

    def SelectObjective(self):
        self.objective = self.id_cmb.currentText().strip()
        print("RELTATED:\n\t", self.memRules.GetRelatedRules(self.objective))
        direct = QuestionWidget(self.objective, self)

class QuestionWidget(QWidget):
    """Widget for creating and answering the questions that are needed in the reasoning"""
    def __init__(self, objective, parent = None):
        super(QuestionWidget, self).__init__(parent)
        self.memRules = Rules("rulelist.json")
        self.objective = objective
        
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

        self.setLayout(self.main_layout)
        self.setWindowTitle("Objective Reasoning - Questioning")
        self.show()
        
    def Replace(self):
        print("RELTATED:\n\t", self.memRules.GetRelatedRules(self.objective))

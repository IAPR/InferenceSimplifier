from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from compiler import Compiler

# Two labels
# Two Textboxes
# One button
# One multi-line text box (read-only)
class InferenceSolver(QWidget):
    def __init__(self, parent=None):
        super(InferenceSolver, self).__init__(parent)

        self.inst_lbl = QLabel("Escribe una sentencia antecedente->consecuente")
        self.mid_lbl = QLabel("->")

        self.antecedents = QLineEdit()
        self.consequents = QLineEdit()

        self.refresh_button = QPushButton("Evaluate!")

        self.ant_results = QPlainTextEdit()
        self.con_results = QPlainTextEdit()
        self.ant_results.setReadOnly(True)
        self.con_results.setReadOnly(True)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.antecedents)
        self.hlayout.addWidget(self.mid_lbl)
        self.hlayout.addWidget(self.consequents)
        self.hlayout.addWidget(self.refresh_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.inst_lbl, 0, 0)
        self.main_layout.addLayout(self.hlayout, 1, 0)
        self.main_layout.addWidget(self.ant_results, 2, 0)
        self.main_layout.addWidget(self.con_results, 3, 0)

        self.refresh_button.clicked.connect(self.Evaluate)

        self.setLayout(self.main_layout)
        self.setWindowTitle("My first expert system")

    def Evaluate(self):
        ant_statement = self.antecedents.text().strip()
        if(ant_statement != ""):
            print("Antecedents:", ant_statement)
            ant_ev = Compiler()
            ant_ev.ParseStatement(ant_statement)
            ant_ev.PrintTree()

        con_statement = self.consequents.text().strip()
        if(con_statement != ""):
            print("Consequents:", con_statement)
            con_ev = Compiler()
            con_ev.ParseStatement(con_statement)
            con_ev.PrintTree()

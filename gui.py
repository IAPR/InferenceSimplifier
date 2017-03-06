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

        self.results = QPlainTextEdit()
        self.results.setReadOnly(True)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.antecedents)
        self.hlayout.addWidget(self.mid_lbl)
        self.hlayout.addWidget(self.consequents)
        self.hlayout.addWidget(self.refresh_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.inst_lbl, 0, 0)
        self.main_layout.addLayout(self.hlayout, 1, 0)
        self.main_layout.addWidget(self.results, 2, 0)

        self.refresh_button.clicked.connect(self.Evaluate)

        self.setLayout(self.main_layout)
        self.setWindowTitle("My first expert system")

    def Evaluate(self):
        print("Antecedents:", self.antecedents.text())
        ant_ev = Compiler()
        ant_ev.ParseStatement(self.antecedents.text())
        print("Consequents:", self.consequents.text())
        con_ev = Compiler()


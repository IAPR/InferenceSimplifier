from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from antecedent import Antecedent
from consequent import Consequent
from rule import Rule
from workmemory import WorkMemory

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
        self.statements = QPlainTextEdit()

        self.ant_results.setReadOnly(True)
        self.con_results.setReadOnly(True)
        self.statements.setReadOnly(True)

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
        self.main_layout.addWidget(self.statements, 4, 0)

        self.refresh_button.clicked.connect(self.Evaluate)

        # TEST 1
        self.antecedents.setText("(!(a <-> b) -> (c <-> d))")
        self.consequents.setText("(e<->f)")
        # TEST 2
        # self.antecedents.setText("(!(a <-> b) -> (c <-> d) )")
        # self.consequents.setText("e")

        self.setLayout(self.main_layout)
        self.setWindowTitle("My first expert system")

    def Evaluate(self):
        ant_statement = self.antecedents.text().strip()
        con_statement = self.consequents.text().strip()

        if(ant_statement == "" or con_statement == ""):
            raise Exception

        ant_str = "Antecedents:\n"
        ant_ev = Antecedent(ant_statement)
        ant_str += str(ant_ev) + "\n"
        ant_ev.SimplifyFND()
        ant_str += "Simplified: \n"
        ant_str += str(ant_ev) + "\n"
        self.ant_results.setPlainText(ant_str)

        con_str = "Consequents:\n"
        con_ev = Consequent(con_statement)
        con_str += str(con_ev) + "\n"
        con_ev.SimplifyFNC()
        con_str += "Simplified: \n"
        con_str += str(con_ev) + "\n"
        self.con_results.setPlainText(con_str)

        ant_root = ant_ev.root
        con_root = con_ev.root
        ants = ant_ev.Branch()
        cons = con_ev.Branch()

        print(ants, ant_root)
        print(cons, con_root)

        rules = []
        for a in ants:
            for c in cons:
                rules += Rule.TranslateToRules(a, c)
        rstr = ""

        mem = WorkMemory("rules.json")
        for r in rules:
            rstr += str(r) + "\n"
            print(r)
            print(repr(r))
            mem.AddRule(r)
        mem.Save()
        self.statements.setPlainText(rstr)

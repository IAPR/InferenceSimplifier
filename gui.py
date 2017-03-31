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
        self.id_lbl = QLabel("Id:")
        self.val_lbl = QLabel("Value:")

        self.antecedents = QLineEdit()
        self.consequents = QLineEdit()
        self.variable = QLineEdit()

        self.values = QComboBox()
        self.values.addItem("T")
        self.values.addItem("F")

        self.refresh_button = QPushButton("Evaluate!")
        self.propagate_button = QPushButton("Propagate!")

        self.statements = QPlainTextEdit()
        self.rules = QPlainTextEdit()

        self.statements.setReadOnly(True)
        self.rules.setReadOnly(True)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.antecedents)
        self.hlayout.addWidget(self.mid_lbl)
        self.hlayout.addWidget(self.consequents)
        self.hlayout.addWidget(self.refresh_button)

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.id_lbl)
        self.hlayout2.addWidget(self.variable)
        self.hlayout2.addWidget(self.val_lbl)
        self.hlayout2.addWidget(self.values)
        self.hlayout2.addWidget(self.propagate_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.inst_lbl, 0, 0)
        self.main_layout.addLayout(self.hlayout, 1, 0)
        self.main_layout.addWidget(self.statements, 2, 0)
        self.main_layout.addLayout(self.hlayout2, 3, 0)
        self.main_layout.addWidget(self.rules, 4, 0)

        self.refresh_button.clicked.connect(self.Evaluate)
        self.propagate_button.clicked.connect(self.Propagation)

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

        con_str = "Consequents:\n"
        con_ev = Consequent(con_statement)
        con_str += str(con_ev) + "\n"
        con_ev.SimplifyFNC()
        con_str += "Simplified: \n"
        con_str += str(con_ev) + "\n"

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

        self.memory = WorkMemory("rules.json")
        for r in rules:
            rstr += str(r) + "\n"
            print(r)
            print(repr(r))
            self.memory.AddRule(r)
        self.memory.Save()
        self.statements.setPlainText(rstr)

    def Propagation(self):
        var = self.variable.text().strip()
        value = self.values.currentText().strip()
        self.memory.Propagate(var, value)

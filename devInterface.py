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
class DeveloperInterface(QWidget):
    def __init__(self, parent=None):
        super(DeveloperInterface, self).__init__(parent)

        self.memory = WorkMemory("rules.json")

        self.inst_lbl = QLabel("Escribe una sentencia antecedente->consecuente")
        self.mid_lbl = QLabel("->")
        self.id_lbl = QLabel("Id:")
        self.val_lbl = QLabel("Value:")
        self.solv_lbl = QLabel("No se ha llegado a una solucion")

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
        self.solutions = QPlainTextEdit()

        self.statements.setReadOnly(True)
        self.rules.setReadOnly(True)
        self.solutions = QPlainTextEdit()

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
        self.main_layout.addWidget(self.solv_lbl, 5, 0)
        self.main_layout.addWidget(self.solutions, 6, 0)

        self.refresh_button.clicked.connect(self.Evaluate)
        self.propagate_button.clicked.connect(self.Propagation)

        self.setLayout(self.main_layout)
        self.setWindowTitle("My first expert system")
        self.UpdateCache()
        self.PrintWorkMemory()

    def Evaluate(self):
        ant_statement = self.antecedents.text().strip()
        con_statement = self.consequents.text().strip()

        if(ant_statement == "" or con_statement == ""):
            return

        ant_ev = Antecedent(ant_statement)
        ant_ev.SimplifyFND()
        con_ev = Consequent(con_statement)
        con_ev.SimplifyFNC()

        ants = ant_ev.Branch()
        cons = con_ev.Branch()

        rules = []
        for a in ants:
            for c in cons:
                rules += Rule.TranslateToRules(a, c)
        rstr = ""

        print("ANTBRANCHES:")
        for ant in ants:
            print("\t", ant)
        print("CONBRANCHES:")
        for con in cons:
            print("\t", con)

        for r in rules:
            print("RULE:", r)
            self.memory.AddRule(r.consequent, r.antecedent)
        self.memory.Save()
        self.UpdateCache()
        self.PrintWorkMemory()

    def UpdateCache(self):
        self.workmem = self.memory.copy()
        self.rules.setPlainText( str(self.workmem) )

    def PrintWorkMemory(self):
        self.statements.setPlainText( str(self.memory) )

    def Propagation(self):
        var = self.variable.text().strip()
        value = self.values.currentText().strip()
        self.workmem.Propagate(var, value)

        solutions = self.workmem.GetSolutions()
        rstr = ""
        if(solutions != []):
            for sol in solutions:
                rstr += sol + "\n"
            self.solv_lbl.setText("Se ha llegado a una conclusion")
            self.solutions.setPlainText( rstr )
        print("Solutions:\n", rstr)

        self.rules.setPlainText( str(self.workmem) )


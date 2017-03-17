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
        ant_ev = Compiler()
        ant_ev.ParseStatement(ant_statement)
        ant_str += ant_ev.ConvertToString(ant_ev.root) + "\n"
        ant_ev.SimplifyFND()
        ant_str += "Simplified: \n"
        ant_str += ant_ev.ConvertToString(ant_ev.root) + "\n"
        self.ant_results.setPlainText(ant_str)

        con_str = "Consequents:\n"
        con_ev = Compiler()
        con_ev.ParseStatement(con_statement)
        con_str += con_ev.ConvertToString(con_ev.root) + "\n"
        con_ev.SimplifyFNC()
        con_str += "Simplified: \n"
        con_str += con_ev.ConvertToString(con_ev.root) + "\n"
        self.con_results.setPlainText(con_str)

        ant_root = ant_ev.root
        con_root = con_ev.root
        ants = []
        cons = []

        def FNDBranches(ar):
            ars = []
            if(ar == None):
                return []
            elif(ar.symbol.code == "OP_OR" and ar.sign):
                if(ar.left.symbol.code == "OP_OR" and ar.left.sign):
                    ars = ars + FNDBranches(ar.left)
                else:
                    ars.append(ar.left)
                if(ar.right.symbol.code == "OP_OR" and ar.right.sign):
                    ars = ars + FNDBranches(ar.right)
                else:
                    ars.append(ar.right)
            return ars

        def FNCBranches(ar):
            ars = []
            if(ar == None):
                return []
            elif(ar.symbol.code == "OP_AND" and ar.sign):
                if(ar.left.symbol.code == "OP_AND" and ar.left.sign):
                    ars = ars + FNCBranches(ar.left)
                else:
                    ars.append(ar.left)
                if(ar.right.symbol.code == "OP_AND" and ar.right.sign):
                    ars = ars + FNCBranches(ar.right)
                else:
                    ars.append(ar.right)
            return ars

        ants = FNDBranches(ant_root)
        cons = FNCBranches(con_root)

        if(ants == []):
            ants.append(ant_root)
        if(cons == []):
            cons.append(con_root)

        print(ants, ant_root)
        print(cons, con_root)

        st_str = ""
        for ant in ants:
            for con in cons:
                if(con.symbol.code == "OP_OR"):
                    st_str += ant_ev.ConvertToString(ant) + "^ " 
                    st_str += con_ev.ConvertToString(con.right) + "-> " 
                    st_str += con_ev.ConvertToString(con.left) + "\n"
                    st_str += ant_ev.ConvertToString(ant) + "^ " 
                    st_str += con_ev.ConvertToString(con.left) + "-> " 
                    st_str += con_ev.ConvertToString(con.right) + "\n"
                else:
                    st_str += ant_ev.ConvertToString(ant) + "-> " 
                    st_str += con_ev.ConvertToString(con) + "\n"
        self.statements.setPlainText(st_str)


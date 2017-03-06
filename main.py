#!/usr/bin/python3
from gui import InferenceSolver
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
screen = InferenceSolver()
screen.show()

sys.exit(app.exec_())

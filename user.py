#!/usr/bin/python3
from userInterface import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
obj = ObjectiveWidget()
obj.show()
sys.exit(app.exec_())

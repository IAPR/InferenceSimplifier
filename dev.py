#!/usr/bin/python3
from devInterface import DeveloperInterface
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)
screen = DeveloperInterface()
screen.show()

sys.exit(app.exec_())

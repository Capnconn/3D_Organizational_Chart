from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QCheckBox, QSizePolicy

import sys, os
cur_path = os.getcwd()

import sys, os


# Enables the interfaces to function on higher resolution monitors
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class DeleteBranchPage(QMainWindow):
	def __init__(self):
		super(DeleteBranchPage, self).__init__()

		uic.loadUi(cur_path + "/ui/DeleteBranch.ui", self)

		self.show()


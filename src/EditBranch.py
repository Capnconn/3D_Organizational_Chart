from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QSizePolicy
import sys, os
import AdminLoginPage

# Go back to the previous directory - to acces the ui folder
# os.chdir("..")
cur_path = os.getcwd()

#Enables the interfaces to functions on higher resolution monitors
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class EditBranch(QMainWindow):
	def __init__(self):
		super(EditBranch, self).__init__()

		# Load corresponding ui file
		uic.loadUi(cur_path + "/ui/EditBranch.ui", self)

		# Define our widgets
		self.saveButton = self.findChild(QPushButton, "SaveButton")
		self.homeButton = self.findChild(QPushButton, "HomeButton")
		self.branchEdit = self.findChild(QLineEdit, "BranchValue")
		self.missingFieldLabel = self.findChild(QLabel, "MissingFieldLabel")
		self.label = self.findChild(QLabel, "label")

		# Hide alert message --> only display it when necessary
		self.missingFieldLabel.setHidden(True)

		# Set pointer when either buttons have been hovered over
		self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.homeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

		# Handle edit branch click
		self.saveButton.clicked.connect(self.handleEditBranch)

		# Handle home button click
		self.homeButton.clicked.connect(self.handleHomeClick)

		self.show()

	def handleHomeClick(self):
		self.close()
		nextApp = QApplication(sys.argv)
		homePage = AdminLoginPage.AdminLoginPage()
		nextApp.exec_()

	def handleEditBranch(self):
		if self.branchEdit.text().strip() == '':
			self.missingFieldLabel.setHidden(False)
			return

		self.missingFieldLabel.setHidden(True)
		self.label.setText(self.branchEdit.text())
		return
		

if __name__ == "__main__":
	#Initialize the App
	app = QApplication(sys.argv)
	editBranchWindow = EditBranch()
	app.exec_()
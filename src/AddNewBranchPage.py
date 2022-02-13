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

class AddNewBranchPage(QMainWindow):
	def __init__(self):
		super(AddNewBranchPage, self).__init__()

		# Load corresponding ui file
		uic.loadUi(cur_path + "/ui/AddBranchPage.ui", self)

		# Define our widgets
		self.addBranchButton = self.findChild(QPushButton, "AddBranchButton")
		self.homeButton = self.findChild(QPushButton, "HomeButton")
		self.branchEdit = self.findChild(QLineEdit, "BranchValue")
		self.missingFieldLabel = self.findChild(QLabel, "MissingFieldLabel")

		# Hide alert message --> only display it when necessary
		self.missingFieldLabel.setHidden(True)

		# Set pointer when either buttons have been hovered over
		self.addBranchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.homeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

		# Handle add branch click
		self.addBranchButton.clicked.connect(self.handleNewBranch)

		# Handle home button click
		self.homeButton.clicked.connect(self.handleHomeClick)

		self.show()

	def handleHomeClick(self):
		self.close()
		nextApp = QApplication(sys.argv)
		homePage = AdminLoginPage.AdminLoginPage()
		nextApp.exec_()

	def handleNewBranch(self):
		if self.branchEdit.text().strip() == '':
			self.missingFieldLabel.setHidden(False)
			return

		self.missingFieldLabel.setHidden(True)
		print("New branch name: " + self.branchEdit.text())

if __name__ == "__main__":
	#Initialize the App
	app = QApplication(sys.argv)
	addBranchWindow = AddNewBranchPage()
	app.exec_()

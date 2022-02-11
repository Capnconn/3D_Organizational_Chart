from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
import sys, os

# Go back to the previous directory - to access the ui folder
os.chdir("..")
cur_path = os.getcwd()

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		uic.loadUi(cur_path + "/ui/AdminLoginPage.ui", self)

		# Define our widgets
		self.usernameEdit = self.findChild(QLineEdit, "UsernameValue")
		self.passwordEdit = self.findChild(QLineEdit, "PasswordValue")
		self.loginButton = self.findChild(QPushButton, "LoginButton")
		self.viewButton = self.findChild(QPushButton, "ViewButton")

		# Set pointer when either buttons have been hovered over
		self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.viewButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


		# Handle submit click
		self.loginButton.clicked.connect(self.handleSubmit)

		self.show()

	def handleSubmit(self):
		print("Username: " + self.usernameEdit.text())
		print("Password: " + self.passwordEdit.text())



# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()
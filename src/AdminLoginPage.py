from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QCheckBox, QSizePolicy
import sys, os

# Go back to the previous directory - to access the ui folder
os.chdir("..")
cur_path = os.getcwd()

# Enables the interfaces to function on higher resolution monitors
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		uic.loadUi(cur_path + "/ui/AdminLoginPage.ui", self)

		# Enforce a particular window size, to prevent from empty space
		self.setFixedWidth(600)
		self.setFixedHeight(500)

		# Define our widgets
		self.usernameEdit = self.findChild(QLineEdit, "UsernameValue")
		self.passwordEdit = self.findChild(QLineEdit, "PasswordValue")
		self.loginButton = self.findChild(QPushButton, "LoginButton")
		self.viewButton = self.findChild(QPushButton, "ViewButton")
		self.incorrectField = self.findChild(QLabel, "IncorrectField")
		self.fieldMissing = self.findChild(QLabel, "FieldMissing")
		self.showPassword = self.findChild(QCheckBox, "ShowPassword")

		# Connect a show password function
		self.showPassword.stateChanged.connect(self.unhidePassword)

		# Set password to be hidden
		self.passwordEdit.setEchoMode(QLineEdit.Password)

		# Hide the alert message --> only display it when necessarys
		self.fieldMissing.setHidden(True)
		self.incorrectField.setHidden(True)

		# Set pointer when either buttons have been hovered over
		self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.viewButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


		# Handle submit click
		self.loginButton.clicked.connect(self.handleSubmit)

		self.show()

	# Hide/unhide password based on whether or note checkbox is checked
	def unhidePassword(self):
		if self.passwordEdit.echoMode() == QLineEdit.Normal:
			self.passwordEdit.setEchoMode(QLineEdit.Password)
		else:
			self.passwordEdit.setEchoMode(QLineEdit.Normal)

	def handleSubmit(self):

		# Check if username and password field are filled out
		if self.usernameEdit.text().strip() == '' and self.passwordEdit.text().strip() == '':
			self.fieldMissing.setText("* Username and password field's are required.")
			self.incorrectField.setHidden(True)
			self.fieldMissing.setHidden(False)
			return
		elif self.usernameEdit.text().strip() == '':
			self.fieldMissing.setText("* Username field is required.")
			self.incorrectField.setHidden(True)	
			self.fieldMissing.setHidden(False)
			return
		elif self.passwordEdit.text().strip() == '':
			self.fieldMissing.setText("* Password field is required.")
			self.incorrectField.setHidden(True)
			self.fieldMissing.setHidden(False)
			return
		self.fieldMissing.setHidden(True)

		# Check if credentials are correct
		if not self.usernameEdit.text().strip() == 'Connor' and not self.passwordEdit.text().strip() == 'password':
			self.incorrectField.setHidden(False)
			return

		self.incorrectField.setHidden(True)

		print("Username: " + self.usernameEdit.text())
		print("Password: " + self.passwordEdit.text())



if __name__ == "__main__":
	# Initialize the App
	app = QApplication(sys.argv)
	UIWindow = UI()
	app.exec_()
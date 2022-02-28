from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QCheckBox, QSizePolicy, QMessageBox, QComboBox
import sys, os

# Go back to the previous directory - to access the ui folder
os.chdir("..")
cur_path = os.getcwd()

# Enables the interfaces to function on higher resolution monitors
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class DeletePage(QMainWindow):
	def __init__(self):
		super(DeletePage, self).__init__()

		uic.loadUi(cur_path + "/ui/DeletePage.ui", self)

		# Enforce a particular window size, to prevent from empty space
		self.setFixedWidth(600)
		self.setFixedHeight(500)

		# Define our widgets
		self.comboBox = self.findChild(QComboBox, "comboBox")
		self.deleteButton = self.findChild(QPushButton, "deleteButton")
		
		self.comboBox.currentTextChanged.connect(self.onComboBoxChanged)
		self.deleteButton.clicked.connect(self.displayInfoMsg)
		
		self.show()
		
	#Stores selected option into variable to be displayed in delete message
	def onComboBoxChanged (text):
		deletedConnection = text
		return deletedConnection
	
	#Tells user that connection has been deleted successfully. FIXME: take return value from onComboBoxChanged and output in QMessageBox
	def displayInfoMsg(self):
		#deletedConnection = onComboBoxChanged()
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText('The connection has been deleted.')
		msg.exec_()
	
		
	

if __name__ == "__main__":
	# Initialize the App
	app = QApplication(sys.argv)
	DeleteWindow = DeletePage()
	app.exec_()
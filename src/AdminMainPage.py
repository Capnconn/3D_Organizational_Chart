from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QCheckBox, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from qtwidgets import Toggle, AnimatedToggle

import sys, os
cur_path = os.getcwd()

from DeleteBranch import DeleteBranchPage


QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class PyToggle(QCheckBox):
	def __init__(
		self,
		width = 50,
		height = 20,
		bg_color = "grey",
		circle_color = "white",
		active_color = "lightgreen",
		animation_curve = QtCore.QEasingCurve.OutQuint
	):
		QCheckBox.__init__(self)

		# Set default parameters
		self.setFixedSize(width, height)
		self.setCursor(QtCore.Qt.PointingHandCursor)

		# Colors
		self._bg_color = bg_color
		self._circle_color = circle_color
		self._active_color = active_color

		# Create animation
		self._circle_position = 0
		self.animation = QPropertyAnimation(self, b"circle_position", self)
		self.animation.setEasingCurve(animation_curve)
		self.animation.setDuration(500)

		# Connect state changed
		self.stateChanged.connect(self.start_transition)

	@pyqtProperty(int)
	def circle_position(self):
		return self._circle_position

	@circle_position.setter
	def circle_position(self, pos):
		self._circle_position = pos
		self.update()
	
	def start_transition(self, value):
		self.animation.stop()
		if value:
			self.animation.setEndValue(self.width() - 18)
		else:
			self.animation.setEndValue(0)

		# Start animation
		self.animation.start()



	# Set new hit area
	def hitButton(self, pos: QtCore.QPoint):
		return self.contentsRect().contains(pos)


	# Draw new items 
	def paintEvent(self, e):
		# Set painter
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)

		# Set as no pen
		p.setPen(QtCore.Qt.NoPen)

		# Draw Rectangle
		rect = QtCore.QRect(0, 0, self.width(), self.height())

		if not self.isChecked():
			# Draw BG
			p.setBrush(QColor(self._bg_color))
			p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
			# Draw circle
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self.circle_position, 1, self.height()-2, self.height()-2)
		else:
			# Draw BG
			p.setBrush(QColor(self._active_color))
			p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

			# Draw circle
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self.circle_position, 1, self.height()-2, self.height()-2)

		# End draw
		p.end()





class AdminMainPage(QMainWindow):
	def __init__(self):
		super(AdminMainPage, self).__init__()

		uic.loadUi(cur_path + "/ui/AdminMainPage.ui", self)

		# Define our widgets
		self.editBranchButton = self.findChild(QPushButton, "EditBranchButton")
		self.addBranchButton = self.findChild(QPushButton, "AddBranchButton")
		self.deleteBranchButton = self.findChild(QPushButton, "DeleteBranchButton")
		# self.relationshipLayout = QVBoxLayout()
		# self.relationshipLayout.setAlignment(QtCore.Qt.AlignCenter)
		self.relationshipLayout = self.findChild(QVBoxLayout, "RelationshipVertLayout")
		self.toggle = PyToggle()

		self.relationshipLabel = self.findChild(QLabel, "RelationshipLabel")
		self.relationshipLabel.setText("Relationships")

		# self.relationshipLabel = QLabel("Relationships", self)
		self.relationshipLabel.setStyleSheet("background-color: transparent")
		self.relationshipLabel.setFont(QtGui.QFont('Arial', 6))
		self.relationshipLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.relationshipLayout.addWidget(self.toggle, QtCore.Qt.AlignJustify, QtCore.Qt.AlignJustify)
		self.relationshipLayout.addWidget(self.relationshipLabel, QtCore.Qt.AlignTop, QtCore.Qt.AlignTop)

		self.deleteBranchButton.clicked.connect(self.openMainWindow)
		self.show()


	def openMainWindow(self):
		self.window = QtWidgets.QMainWindow()
		self.ui = DeleteBranchPage()
		self.close()

# if __name__ == "__main__":
# 	app = QApplication(sys.argv)
# 	adminMainPage = AdminMainPage()
# 	app.exec_()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Ui_Delete(object):
    def setupUi(self, Delete):
        Delete.setObjectName("Delete")
        Delete.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0.343284 rgba(203, 239, 253, 255), stop:0.840796 rgba(255, 255, 255, 255))")
        self.formLayout = QtWidgets.QFormLayout(Delete)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Delete)
        self.label.setStyleSheet("background-color: rgb(203, 239, 253)")
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(Delete)
        self.comboBox.setStyleSheet("background-color: rgb(211, 215, 207)")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.comboBox)
        self.pushButton = QtWidgets.QPushButton(Delete)
        self.pushButton.setStyleSheet("background-color: rgb(211, 215, 207)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.button_clicked)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pushButton)
        self.label_2 = QtWidgets.QLabel(Delete)
        self.label_2.setStyleSheet("color: rgb(113, 175, 55);\n"
"background-color: rgb(203, 239, 253)")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(Delete)
        QtCore.QMetaObject.connectSlotsByName(Delete)

    def retranslateUi(self, Delete):
        _translate = QtCore.QCoreApplication.translate
        Delete.setWindowTitle(_translate("Delete", "Bayer - Delete"))
        self.label.setText(_translate("Delete", "Choose a Connection:"))
        self.comboBox.setItemText(0, _translate("Delete", "Supply Chain Management Production Management -> Supply Chain Management Development"))
        self.comboBox.setItemText(1, _translate("Delete", "Agile Office -> Supply Chain Management Production Management"))
        self.comboBox.setItemText(2, _translate("Delete", "Agile Office -> Supply Chain Management Development"))
        self.pushButton.setText(_translate("Delete", "Delete"))
        self.label_2.setText(_translate("Delete", "<html><head/><body><p><span style=\" font-size:24pt;\">Bayer</span></p></body></html>"))

    def button_clicked(self):	
        msg = QMessageBox()
        msg.setText("The connection was successfully deleted.")
        msg.setWindowTitle("Connection Deleted")
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Delete = QtWidgets.QDialog()
    ui = Ui_Delete()
    ui.setupUi(Delete)
    Delete.show()
    sys.exit(app.exec_())

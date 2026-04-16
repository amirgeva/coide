# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/deps.ui'
#
#
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets

def _fromUtf8(s):
    return s

def _translate(context, text, disambig):
    return QtCore.QCoreApplication.translate(context, text)

class Ui_dependenciesDialog(object):
    def setupUi(self, dependenciesDialog):
        dependenciesDialog.setObjectName(_fromUtf8("dependenciesDialog"))
        dependenciesDialog.resize(415, 285)
        dependenciesDialog.depsList = QtWidgets.QListWidget(dependenciesDialog)
        dependenciesDialog.depsList.setGeometry(QtCore.QRect(10, 10, 361, 231))
        dependenciesDialog.depsList.setObjectName(_fromUtf8("depsList"))
        dependenciesDialog.upButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.upButton.setGeometry(QtCore.QRect(380, 10, 31, 31))
        dependenciesDialog.upButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/up.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dependenciesDialog.upButton.setIcon(icon)
        dependenciesDialog.upButton.setObjectName(_fromUtf8("upButton"))
        dependenciesDialog.downButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.downButton.setGeometry(QtCore.QRect(380, 50, 31, 31))
        dependenciesDialog.downButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("icons/down.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dependenciesDialog.downButton.setIcon(icon1)
        dependenciesDialog.downButton.setObjectName(_fromUtf8("downButton"))
        dependenciesDialog.okButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.okButton.setGeometry(QtCore.QRect(10, 250, 85, 27))
        dependenciesDialog.okButton.setObjectName(_fromUtf8("okButton"))
        dependenciesDialog.cancelButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.cancelButton.setGeometry(QtCore.QRect(100, 250, 85, 27))
        dependenciesDialog.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        dependenciesDialog.addButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.addButton.setGeometry(QtCore.QRect(200, 250, 85, 27))
        dependenciesDialog.addButton.setObjectName(_fromUtf8("addButton"))
        dependenciesDialog.removeButton = QtWidgets.QPushButton(dependenciesDialog)
        dependenciesDialog.removeButton.setGeometry(QtCore.QRect(290, 250, 85, 27))
        dependenciesDialog.removeButton.setObjectName(_fromUtf8("removeButton"))

        self.retranslateUi(dependenciesDialog)
        QtCore.QMetaObject.connectSlotsByName(dependenciesDialog)

    def retranslateUi(self, dependenciesDialog):
        dependenciesDialog.setWindowTitle(_translate("dependenciesDialog", "Dependencies", None))
        dependenciesDialog.okButton.setText(_translate("dependenciesDialog", "Ok", None))
        dependenciesDialog.cancelButton.setText(_translate("dependenciesDialog", "Cancel", None))
        dependenciesDialog.addButton.setText(_translate("dependenciesDialog", "Add", None))
        dependenciesDialog.removeButton.setText(_translate("dependenciesDialog", "Remove", None))


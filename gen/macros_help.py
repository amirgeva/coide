# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/macros_help.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        Dialog.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        Dialog.buttonBox.setGeometry(QtCore.QRect(50, 260, 341, 32))
        Dialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        Dialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        Dialog.macrosTable = QtWidgets.QTableWidget(Dialog)
        Dialog.macrosTable.setGeometry(QtCore.QRect(10, 10, 381, 241))
        Dialog.macrosTable.setObjectName(_fromUtf8("macrosTable"))
        Dialog.macrosTable.setColumnCount(0)
        Dialog.macrosTable.setRowCount(0)
        Dialog.macrosTable.horizontalHeader().setVisible(True)
        Dialog.macrosTable.horizontalHeader().setStretchLastSection(True)
        Dialog.macrosTable.verticalHeader().setVisible(False)

        self.retranslateUi(Dialog)
        Dialog.buttonBox.accepted.connect(Dialog.accept)
        Dialog.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Macros Help", None))


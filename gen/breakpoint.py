# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/breakpoint.ui'
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
        Dialog.buttonBox.setGeometry(QtCore.QRect(40, 260, 341, 32))
        Dialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        Dialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        Dialog.condition = QtWidgets.QLineEdit(Dialog)
        Dialog.condition.setGeometry(QtCore.QRect(90, 10, 301, 27))
        Dialog.condition.setObjectName(_fromUtf8("condition"))
        Dialog.label = QtWidgets.QLabel(Dialog)
        Dialog.label.setGeometry(QtCore.QRect(20, 10, 71, 17))
        Dialog.label.setObjectName(_fromUtf8("label"))
        Dialog.enabled = QtWidgets.QCheckBox(Dialog)
        Dialog.enabled.setGeometry(QtCore.QRect(20, 50, 88, 22))
        Dialog.enabled.setObjectName(_fromUtf8("enabled"))

        self.retranslateUi(Dialog)
        Dialog.buttonBox.accepted.connect(Dialog.accept)
        Dialog.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Breakpoint", None))
        Dialog.label.setText(_translate("Dialog", "Condition:", None))
        Dialog.enabled.setText(_translate("Dialog", "Enabled", None))


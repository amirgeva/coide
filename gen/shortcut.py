# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/shortcut.ui'
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

class Ui_ShortcutDialog(object):
    def setupUi(self, ShortcutDialog):
        ShortcutDialog.setObjectName(_fromUtf8("ShortcutDialog"))
        ShortcutDialog.resize(251, 236)
        ShortcutDialog.buttonBox = QtWidgets.QDialogButtonBox(ShortcutDialog)
        ShortcutDialog.buttonBox.setGeometry(QtCore.QRect(30, 190, 181, 32))
        ShortcutDialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        ShortcutDialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ShortcutDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        ShortcutDialog.keyCB = QtWidgets.QComboBox(ShortcutDialog)
        ShortcutDialog.keyCB.setGeometry(QtCore.QRect(100, 20, 131, 33))
        ShortcutDialog.keyCB.setObjectName(_fromUtf8("keyCB"))
        ShortcutDialog.label = QtWidgets.QLabel(ShortcutDialog)
        ShortcutDialog.label.setGeometry(QtCore.QRect(20, 20, 56, 17))
        ShortcutDialog.label.setObjectName(_fromUtf8("label"))
        ShortcutDialog.ctrlCB = QtWidgets.QCheckBox(ShortcutDialog)
        ShortcutDialog.ctrlCB.setGeometry(QtCore.QRect(20, 60, 88, 22))
        ShortcutDialog.ctrlCB.setObjectName(_fromUtf8("ctrlCB"))
        ShortcutDialog.altCB = QtWidgets.QCheckBox(ShortcutDialog)
        ShortcutDialog.altCB.setGeometry(QtCore.QRect(20, 90, 88, 22))
        ShortcutDialog.altCB.setObjectName(_fromUtf8("altCB"))
        ShortcutDialog.shiftCB = QtWidgets.QCheckBox(ShortcutDialog)
        ShortcutDialog.shiftCB.setGeometry(QtCore.QRect(20, 120, 88, 22))
        ShortcutDialog.shiftCB.setObjectName(_fromUtf8("shiftCB"))
        ShortcutDialog.metaCB = QtWidgets.QCheckBox(ShortcutDialog)
        ShortcutDialog.metaCB.setGeometry(QtCore.QRect(20, 150, 88, 22))
        ShortcutDialog.metaCB.setObjectName(_fromUtf8("metaCB"))

        self.retranslateUi(ShortcutDialog)
        ShortcutDialog.buttonBox.accepted.connect(ShortcutDialog.accept)
        ShortcutDialog.buttonBox.rejected.connect(ShortcutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ShortcutDialog)

    def retranslateUi(self, ShortcutDialog):
        ShortcutDialog.setWindowTitle(_translate("ShortcutDialog", "Keyboard Shortcut", None))
        ShortcutDialog.label.setText(_translate("ShortcutDialog", "Key:", None))
        ShortcutDialog.ctrlCB.setText(_translate("ShortcutDialog", "Ctrl", None))
        ShortcutDialog.altCB.setText(_translate("ShortcutDialog", "Alt", None))
        ShortcutDialog.shiftCB.setText(_translate("ShortcutDialog", "Shift", None))
        ShortcutDialog.metaCB.setText(_translate("ShortcutDialog", "Meta", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/shortcut.ui'
#
#
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ShortcutDialog(object):
    def setupUi(self, ShortcutDialog):
        ShortcutDialog.setObjectName(_fromUtf8("ShortcutDialog"))
        ShortcutDialog.resize(251, 236)
        ShortcutDialog.buttonBox = QtGui.QDialogButtonBox(ShortcutDialog)
        ShortcutDialog.buttonBox.setGeometry(QtCore.QRect(30, 190, 181, 32))
        ShortcutDialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        ShortcutDialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        ShortcutDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        ShortcutDialog.keyCB = QtGui.QComboBox(ShortcutDialog)
        ShortcutDialog.keyCB.setGeometry(QtCore.QRect(100, 20, 131, 33))
        ShortcutDialog.keyCB.setObjectName(_fromUtf8("keyCB"))
        ShortcutDialog.label = QtGui.QLabel(ShortcutDialog)
        ShortcutDialog.label.setGeometry(QtCore.QRect(20, 20, 56, 17))
        ShortcutDialog.label.setObjectName(_fromUtf8("label"))
        ShortcutDialog.ctrlCB = QtGui.QCheckBox(ShortcutDialog)
        ShortcutDialog.ctrlCB.setGeometry(QtCore.QRect(20, 60, 88, 22))
        ShortcutDialog.ctrlCB.setObjectName(_fromUtf8("ctrlCB"))
        ShortcutDialog.altCB = QtGui.QCheckBox(ShortcutDialog)
        ShortcutDialog.altCB.setGeometry(QtCore.QRect(20, 90, 88, 22))
        ShortcutDialog.altCB.setObjectName(_fromUtf8("altCB"))
        ShortcutDialog.shiftCB = QtGui.QCheckBox(ShortcutDialog)
        ShortcutDialog.shiftCB.setGeometry(QtCore.QRect(20, 120, 88, 22))
        ShortcutDialog.shiftCB.setObjectName(_fromUtf8("shiftCB"))
        ShortcutDialog.metaCB = QtGui.QCheckBox(ShortcutDialog)
        ShortcutDialog.metaCB.setGeometry(QtCore.QRect(20, 150, 88, 22))
        ShortcutDialog.metaCB.setObjectName(_fromUtf8("metaCB"))

        self.retranslateUi(ShortcutDialog)
        QtCore.QObject.connect(ShortcutDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ShortcutDialog.accept)
        QtCore.QObject.connect(ShortcutDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ShortcutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ShortcutDialog)

    def retranslateUi(self, ShortcutDialog):
        ShortcutDialog.setWindowTitle(_translate("ShortcutDialog", "Keyboard Shortcut", None))
        ShortcutDialog.label.setText(_translate("ShortcutDialog", "Key:", None))
        ShortcutDialog.ctrlCB.setText(_translate("ShortcutDialog", "Ctrl", None))
        ShortcutDialog.altCB.setText(_translate("ShortcutDialog", "Alt", None))
        ShortcutDialog.shiftCB.setText(_translate("ShortcutDialog", "Shift", None))
        ShortcutDialog.metaCB.setText(_translate("ShortcutDialog", "Meta", None))


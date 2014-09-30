# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/debug_settings.ui'
#
# Created: Tue Sep 30 12:44:23 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_DebugSettingsDialog(object):
    def setupUi(self, DebugSettingsDialog):
        DebugSettingsDialog.setObjectName(_fromUtf8("DebugSettingsDialog"))
        DebugSettingsDialog.resize(453, 147)
        DebugSettingsDialog.buttonBox = QtGui.QDialogButtonBox(DebugSettingsDialog)
        DebugSettingsDialog.buttonBox.setGeometry(QtCore.QRect(90, 100, 341, 32))
        DebugSettingsDialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        DebugSettingsDialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        DebugSettingsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        DebugSettingsDialog.cwdEdit = QtGui.QLineEdit(DebugSettingsDialog)
        DebugSettingsDialog.cwdEdit.setGeometry(QtCore.QRect(150, 10, 251, 27))
        DebugSettingsDialog.cwdEdit.setObjectName(_fromUtf8("cwdEdit"))
        DebugSettingsDialog.label = QtGui.QLabel(DebugSettingsDialog)
        DebugSettingsDialog.label.setGeometry(QtCore.QRect(10, 10, 131, 17))
        DebugSettingsDialog.label.setObjectName(_fromUtf8("label"))
        DebugSettingsDialog.paramsEdit = QtGui.QLineEdit(DebugSettingsDialog)
        DebugSettingsDialog.paramsEdit.setGeometry(QtCore.QRect(150, 50, 291, 27))
        DebugSettingsDialog.paramsEdit.setObjectName(_fromUtf8("paramsEdit"))
        DebugSettingsDialog.label_2 = QtGui.QLabel(DebugSettingsDialog)
        DebugSettingsDialog.label_2.setGeometry(QtCore.QRect(10, 50, 111, 17))
        DebugSettingsDialog.label_2.setObjectName(_fromUtf8("label_2"))
        DebugSettingsDialog.browseDirButton = QtGui.QPushButton(DebugSettingsDialog)
        DebugSettingsDialog.browseDirButton.setGeometry(QtCore.QRect(410, 10, 31, 27))
        DebugSettingsDialog.browseDirButton.setObjectName(_fromUtf8("browseDirButton"))

        self.retranslateUi(DebugSettingsDialog)
        QtCore.QObject.connect(DebugSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DebugSettingsDialog.accept)
        QtCore.QObject.connect(DebugSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DebugSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DebugSettingsDialog)

    def retranslateUi(self, DebugSettingsDialog):
        DebugSettingsDialog.setWindowTitle(_translate("DebugSettingsDialog", "Debug Settings", None))
        DebugSettingsDialog.label.setText(_translate("DebugSettingsDialog", "Working Directory", None))
        DebugSettingsDialog.label_2.setText(_translate("DebugSettingsDialog", "Parameters", None))
        DebugSettingsDialog.browseDirButton.setText(_translate("DebugSettingsDialog", "...", None))


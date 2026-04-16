# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/debug_settings.ui'
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

class Ui_DebugSettingsDialog(object):
    def setupUi(self, DebugSettingsDialog):
        DebugSettingsDialog.setObjectName(_fromUtf8("DebugSettingsDialog"))
        DebugSettingsDialog.resize(453, 147)
        DebugSettingsDialog.buttonBox = QtWidgets.QDialogButtonBox(DebugSettingsDialog)
        DebugSettingsDialog.buttonBox.setGeometry(QtCore.QRect(90, 100, 341, 32))
        DebugSettingsDialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        DebugSettingsDialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        DebugSettingsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        DebugSettingsDialog.cwdEdit = QtWidgets.QLineEdit(DebugSettingsDialog)
        DebugSettingsDialog.cwdEdit.setGeometry(QtCore.QRect(150, 10, 251, 27))
        DebugSettingsDialog.cwdEdit.setObjectName(_fromUtf8("cwdEdit"))
        DebugSettingsDialog.label = QtWidgets.QLabel(DebugSettingsDialog)
        DebugSettingsDialog.label.setGeometry(QtCore.QRect(10, 10, 131, 17))
        DebugSettingsDialog.label.setObjectName(_fromUtf8("label"))
        DebugSettingsDialog.paramsEdit = QtWidgets.QLineEdit(DebugSettingsDialog)
        DebugSettingsDialog.paramsEdit.setGeometry(QtCore.QRect(150, 50, 291, 27))
        DebugSettingsDialog.paramsEdit.setObjectName(_fromUtf8("paramsEdit"))
        DebugSettingsDialog.label_2 = QtWidgets.QLabel(DebugSettingsDialog)
        DebugSettingsDialog.label_2.setGeometry(QtCore.QRect(10, 50, 111, 17))
        DebugSettingsDialog.label_2.setObjectName(_fromUtf8("label_2"))
        DebugSettingsDialog.browseDirButton = QtWidgets.QPushButton(DebugSettingsDialog)
        DebugSettingsDialog.browseDirButton.setGeometry(QtCore.QRect(410, 10, 31, 27))
        DebugSettingsDialog.browseDirButton.setObjectName(_fromUtf8("browseDirButton"))

        self.retranslateUi(DebugSettingsDialog)
        DebugSettingsDialog.buttonBox.accepted.connect(DebugSettingsDialog.accept)
        DebugSettingsDialog.buttonBox.rejected.connect(DebugSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DebugSettingsDialog)

    def retranslateUi(self, DebugSettingsDialog):
        DebugSettingsDialog.setWindowTitle(_translate("DebugSettingsDialog", "Debug Settings", None))
        DebugSettingsDialog.label.setText(_translate("DebugSettingsDialog", "Working Directory", None))
        DebugSettingsDialog.label_2.setText(_translate("DebugSettingsDialog", "Parameters", None))
        DebugSettingsDialog.browseDirButton.setText(_translate("DebugSettingsDialog", "...", None))


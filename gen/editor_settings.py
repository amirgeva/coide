# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/editor_settings.ui'
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

class Ui_EditorSettingsDialog(object):
    def setupUi(self, EditorSettingsDialog):
        EditorSettingsDialog.setObjectName(_fromUtf8("EditorSettingsDialog"))
        EditorSettingsDialog.resize(640, 480)
        EditorSettingsDialog.buttonBox = QtWidgets.QDialogButtonBox(EditorSettingsDialog)
        EditorSettingsDialog.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        EditorSettingsDialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        EditorSettingsDialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        EditorSettingsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        EditorSettingsDialog.indentSpaces = QtWidgets.QLineEdit(EditorSettingsDialog)
        EditorSettingsDialog.indentSpaces.setGeometry(QtCore.QRect(180, 20, 113, 32))
        EditorSettingsDialog.indentSpaces.setObjectName(_fromUtf8("indentSpaces"))
        EditorSettingsDialog.label = QtWidgets.QLabel(EditorSettingsDialog)
        EditorSettingsDialog.label.setGeometry(QtCore.QRect(20, 20, 151, 22))
        EditorSettingsDialog.label.setObjectName(_fromUtf8("label"))
        EditorSettingsDialog.clangCB = QtWidgets.QCheckBox(EditorSettingsDialog)
        EditorSettingsDialog.clangCB.setGeometry(QtCore.QRect(16, 64, 321, 27))
        EditorSettingsDialog.clangCB.setObjectName(_fromUtf8("clangCB"))

        self.retranslateUi(EditorSettingsDialog)
        EditorSettingsDialog.buttonBox.accepted.connect(EditorSettingsDialog.accept)
        EditorSettingsDialog.buttonBox.rejected.connect(EditorSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditorSettingsDialog)

    def retranslateUi(self, EditorSettingsDialog):
        EditorSettingsDialog.setWindowTitle(_translate("EditorSettingsDialog", "Editor Settings", None))
        EditorSettingsDialog.label.setText(_translate("EditorSettingsDialog", "Indent Spaces", None))
        EditorSettingsDialog.clangCB.setText(_translate("EditorSettingsDialog", "Clang auto-complete", None))


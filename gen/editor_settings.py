# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/editor_settings.ui'
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

class Ui_EditorSettingsDialog(object):
    def setupUi(self, EditorSettingsDialog):
        EditorSettingsDialog.setObjectName(_fromUtf8("EditorSettingsDialog"))
        EditorSettingsDialog.resize(640, 480)
        EditorSettingsDialog.buttonBox = QtGui.QDialogButtonBox(EditorSettingsDialog)
        EditorSettingsDialog.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        EditorSettingsDialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        EditorSettingsDialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        EditorSettingsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        EditorSettingsDialog.indentSpaces = QtGui.QLineEdit(EditorSettingsDialog)
        EditorSettingsDialog.indentSpaces.setGeometry(QtCore.QRect(180, 20, 113, 32))
        EditorSettingsDialog.indentSpaces.setObjectName(_fromUtf8("indentSpaces"))
        EditorSettingsDialog.label = QtGui.QLabel(EditorSettingsDialog)
        EditorSettingsDialog.label.setGeometry(QtCore.QRect(20, 20, 151, 22))
        EditorSettingsDialog.label.setObjectName(_fromUtf8("label"))
        EditorSettingsDialog.clangCB = QtGui.QCheckBox(EditorSettingsDialog)
        EditorSettingsDialog.clangCB.setGeometry(QtCore.QRect(16, 64, 321, 27))
        EditorSettingsDialog.clangCB.setObjectName(_fromUtf8("clangCB"))

        self.retranslateUi(EditorSettingsDialog)
        QtCore.QObject.connect(EditorSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditorSettingsDialog.accept)
        QtCore.QObject.connect(EditorSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditorSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditorSettingsDialog)

    def retranslateUi(self, EditorSettingsDialog):
        EditorSettingsDialog.setWindowTitle(_translate("EditorSettingsDialog", "Editor Settings", None))
        EditorSettingsDialog.label.setText(_translate("EditorSettingsDialog", "Indent Spaces", None))
        EditorSettingsDialog.clangCB.setText(_translate("EditorSettingsDialog", "Clang auto-complete", None))


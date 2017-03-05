# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/general_settings.ui'
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
        EditorSettingsDialog.sortFilesCB = QtGui.QCheckBox(EditorSettingsDialog)
        EditorSettingsDialog.sortFilesCB.setGeometry(QtCore.QRect(10, 20, 321, 27))
        EditorSettingsDialog.sortFilesCB.setObjectName(_fromUtf8("sortFilesCB"))
        EditorSettingsDialog.clearCacheButton = QtGui.QPushButton(EditorSettingsDialog)
        EditorSettingsDialog.clearCacheButton.setGeometry(QtCore.QRect(20, 90, 85, 27))
        EditorSettingsDialog.clearCacheButton.setObjectName(_fromUtf8("clearCacheButton"))
        EditorSettingsDialog.customPrinters = QtGui.QCheckBox(EditorSettingsDialog)
        EditorSettingsDialog.customPrinters.setGeometry(QtCore.QRect(10, 50, 201, 20))
        EditorSettingsDialog.customPrinters.setObjectName(_fromUtf8("customPrinters"))

        self.retranslateUi(EditorSettingsDialog)
        QtCore.QObject.connect(EditorSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditorSettingsDialog.accept)
        QtCore.QObject.connect(EditorSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditorSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditorSettingsDialog)

    def retranslateUi(self, EditorSettingsDialog):
        EditorSettingsDialog.setWindowTitle(_translate("EditorSettingsDialog", "Editor Settings", None))
        EditorSettingsDialog.sortFilesCB.setText(_translate("EditorSettingsDialog", "Sort by File name", None))
        EditorSettingsDialog.clearCacheButton.setText(_translate("EditorSettingsDialog", "Clear Cache", None))
        EditorSettingsDialog.customPrinters.setText(_translate("EditorSettingsDialog", "Use custom gdb printers", None))


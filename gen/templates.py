# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/templates.ui'
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
        Dialog.resize(640, 480)
        Dialog.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        Dialog.buttonBox.setGeometry(QtCore.QRect(406, 440, 225, 32))
        Dialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        Dialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        Dialog.templatesList = QtWidgets.QListWidget(Dialog)
        Dialog.templatesList.setGeometry(QtCore.QRect(16, 64, 161, 353))
        Dialog.templatesList.setObjectName(_fromUtf8("templatesList"))
        Dialog.codeEdit = QtWidgets.QPlainTextEdit(Dialog)
        Dialog.codeEdit.setGeometry(QtCore.QRect(192, 61, 433, 353))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(12)
        Dialog.codeEdit.setFont(font)
        Dialog.codeEdit.setObjectName(_fromUtf8("codeEdit"))
        Dialog.addButton = QtWidgets.QPushButton(Dialog)
        Dialog.addButton.setGeometry(QtCore.QRect(16, 432, 65, 32))
        Dialog.addButton.setObjectName(_fromUtf8("addButton"))
        Dialog.delButton = QtWidgets.QPushButton(Dialog)
        Dialog.delButton.setGeometry(QtCore.QRect(96, 432, 81, 32))
        Dialog.delButton.setObjectName(_fromUtf8("delButton"))
        Dialog.macrosButton = QtWidgets.QPushButton(Dialog)
        Dialog.macrosButton.setGeometry(QtCore.QRect(258, 420, 101, 25))
        Dialog.macrosButton.setObjectName(_fromUtf8("macrosButton"))
        Dialog.label = QtWidgets.QLabel(Dialog)
        Dialog.label.setGeometry(QtCore.QRect(16, 16, 161, 17))
        Dialog.label.setObjectName(_fromUtf8("label"))
        Dialog.tmplDir = QtWidgets.QLineEdit(Dialog)
        Dialog.tmplDir.setGeometry(QtCore.QRect(192, 16, 369, 27))
        Dialog.tmplDir.setObjectName(_fromUtf8("tmplDir"))
        Dialog.tmplDirBrowseButton = QtWidgets.QPushButton(Dialog)
        Dialog.tmplDirBrowseButton.setGeometry(QtCore.QRect(577, 16, 49, 32))
        Dialog.tmplDirBrowseButton.setObjectName(_fromUtf8("tmplDirBrowseButton"))

        self.retranslateUi(Dialog)
        Dialog.buttonBox.accepted.connect(Dialog.accept)
        Dialog.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Code Templates", None))
        Dialog.addButton.setText(_translate("Dialog", "Add", None))
        Dialog.delButton.setText(_translate("Dialog", "Delete", None))
        Dialog.macrosButton.setText(_translate("Dialog", "Macros Help", None))
        Dialog.label.setText(_translate("Dialog", "Templates Directory:", None))
        Dialog.tmplDirBrowseButton.setText(_translate("Dialog", "...", None))


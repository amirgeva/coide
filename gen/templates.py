# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/templates.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 480)
        Dialog.buttonBox = QtGui.QDialogButtonBox(Dialog)
        Dialog.buttonBox.setGeometry(QtCore.QRect(406, 440, 225, 32))
        Dialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        Dialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        Dialog.templatesList = QtGui.QListWidget(Dialog)
        Dialog.templatesList.setGeometry(QtCore.QRect(16, 64, 161, 353))
        Dialog.templatesList.setObjectName(_fromUtf8("templatesList"))
        Dialog.codeEdit = QtGui.QPlainTextEdit(Dialog)
        Dialog.codeEdit.setGeometry(QtCore.QRect(192, 61, 433, 353))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(12)
        Dialog.codeEdit.setFont(font)
        Dialog.codeEdit.setObjectName(_fromUtf8("codeEdit"))
        Dialog.addButton = QtGui.QPushButton(Dialog)
        Dialog.addButton.setGeometry(QtCore.QRect(16, 432, 65, 32))
        Dialog.addButton.setObjectName(_fromUtf8("addButton"))
        Dialog.delButton = QtGui.QPushButton(Dialog)
        Dialog.delButton.setGeometry(QtCore.QRect(96, 432, 81, 32))
        Dialog.delButton.setObjectName(_fromUtf8("delButton"))
        Dialog.macrosButton = QtGui.QPushButton(Dialog)
        Dialog.macrosButton.setGeometry(QtCore.QRect(258, 420, 101, 25))
        Dialog.macrosButton.setObjectName(_fromUtf8("macrosButton"))
        Dialog.label = QtGui.QLabel(Dialog)
        Dialog.label.setGeometry(QtCore.QRect(16, 16, 161, 17))
        Dialog.label.setObjectName(_fromUtf8("label"))
        Dialog.tmplDir = QtGui.QLineEdit(Dialog)
        Dialog.tmplDir.setGeometry(QtCore.QRect(192, 16, 369, 27))
        Dialog.tmplDir.setObjectName(_fromUtf8("tmplDir"))
        Dialog.tmplDirBrowseButton = QtGui.QPushButton(Dialog)
        Dialog.tmplDirBrowseButton.setGeometry(QtCore.QRect(577, 16, 49, 32))
        Dialog.tmplDirBrowseButton.setObjectName(_fromUtf8("tmplDirBrowseButton"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Code Templates", None))
        Dialog.addButton.setText(_translate("Dialog", "Add", None))
        Dialog.delButton.setText(_translate("Dialog", "Delete", None))
        Dialog.macrosButton.setText(_translate("Dialog", "Macros Help", None))
        Dialog.label.setText(_translate("Dialog", "Templates Directory:", None))
        Dialog.tmplDirBrowseButton.setText(_translate("Dialog", "...", None))


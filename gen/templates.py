# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/templates.ui'
#
#
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
        Dialog.templatesList.setGeometry(QtCore.QRect(16, 16, 161, 401))
        Dialog.templatesList.setObjectName(_fromUtf8("templatesList"))
        Dialog.codeEdit = QtGui.QPlainTextEdit(Dialog)
        Dialog.codeEdit.setGeometry(QtCore.QRect(192, 13, 433, 401))
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

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Code Templates", None))
        Dialog.addButton.setText(_translate("Dialog", "Add", None))
        Dialog.delButton.setText(_translate("Dialog", "Delete", None))


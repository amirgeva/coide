# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/find_replace.ui'
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
        Dialog.resize(400, 300)
        Dialog.label = QtGui.QLabel(Dialog)
        Dialog.label.setGeometry(QtCore.QRect(10, 10, 57, 15))
        Dialog.label.setObjectName(_fromUtf8("label"))
        Dialog.label_2 = QtGui.QLabel(Dialog)
        Dialog.label_2.setGeometry(QtCore.QRect(10, 40, 57, 15))
        Dialog.label_2.setObjectName(_fromUtf8("label_2"))
        Dialog.findEdit = QtGui.QLineEdit(Dialog)
        Dialog.findEdit.setGeometry(QtCore.QRect(90, 10, 231, 21))
        Dialog.findEdit.setObjectName(_fromUtf8("findEdit"))
        Dialog.replaceEdit = QtGui.QLineEdit(Dialog)
        Dialog.replaceEdit.setGeometry(QtCore.QRect(90, 40, 231, 21))
        Dialog.replaceEdit.setObjectName(_fromUtf8("replaceEdit"))
        Dialog.caseCB = QtGui.QCheckBox(Dialog)
        Dialog.caseCB.setGeometry(QtCore.QRect(10, 80, 141, 20))
        Dialog.caseCB.setObjectName(_fromUtf8("caseCB"))
        Dialog.wordsCB = QtGui.QCheckBox(Dialog)
        Dialog.wordsCB.setGeometry(QtCore.QRect(10, 110, 131, 20))
        Dialog.wordsCB.setObjectName(_fromUtf8("wordsCB"))
        Dialog.backCB = QtGui.QCheckBox(Dialog)
        Dialog.backCB.setGeometry(QtCore.QRect(10, 140, 131, 20))
        Dialog.backCB.setObjectName(_fromUtf8("backCB"))
        Dialog.allCB = QtGui.QCheckBox(Dialog)
        Dialog.allCB.setGeometry(QtCore.QRect(10, 170, 131, 20))
        Dialog.allCB.setObjectName(_fromUtf8("allCB"))
        Dialog.findButton = QtGui.QPushButton(Dialog)
        Dialog.findButton.setGeometry(QtCore.QRect(130, 260, 79, 25))
        Dialog.findButton.setDefault(True)
        Dialog.findButton.setObjectName(_fromUtf8("findButton"))
        Dialog.replaceButton = QtGui.QPushButton(Dialog)
        Dialog.replaceButton.setGeometry(QtCore.QRect(220, 260, 79, 25))
        Dialog.replaceButton.setObjectName(_fromUtf8("replaceButton"))
        Dialog.cancelButton = QtGui.QPushButton(Dialog)
        Dialog.cancelButton.setGeometry(QtCore.QRect(310, 260, 79, 25))
        Dialog.cancelButton.setObjectName(_fromUtf8("cancelButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Find / Replace", None))
        Dialog.label.setText(_translate("Dialog", "Find:", None))
        Dialog.label_2.setText(_translate("Dialog", "Replace:", None))
        Dialog.caseCB.setText(_translate("Dialog", "Ignore Case", None))
        Dialog.wordsCB.setText(_translate("Dialog", "Whole Words", None))
        Dialog.backCB.setText(_translate("Dialog", "Find Backwards", None))
        Dialog.allCB.setText(_translate("Dialog", "Replace All", None))
        Dialog.findButton.setText(_translate("Dialog", "Find", None))
        Dialog.replaceButton.setText(_translate("Dialog", "Replace", None))
        Dialog.cancelButton.setText(_translate("Dialog", "Cancel", None))


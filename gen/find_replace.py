# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/find_replace.ui'
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
        Dialog.resize(400, 300)
        Dialog.buttonBox = QtGui.QDialogButtonBox(Dialog)
        Dialog.buttonBox.setGeometry(QtCore.QRect(220, 260, 171, 32))
        Dialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        Dialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        Dialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
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

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(Dialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Find / Replace", None))
        Dialog.label.setText(_translate("Dialog", "Find:", None))
        Dialog.label_2.setText(_translate("Dialog", "Replace:", None))
        Dialog.caseCB.setText(_translate("Dialog", "Ignore Case", None))
        Dialog.wordsCB.setText(_translate("Dialog", "Whole Words", None))
        Dialog.backCB.setText(_translate("Dialog", "Find Backwards", None))
        Dialog.allCB.setText(_translate("Dialog", "Replace All", None))


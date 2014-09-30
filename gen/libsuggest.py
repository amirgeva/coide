# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/libsuggest.ui'
#
# Created: Tue Sep 30 19:39:29 2014
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

class Ui_LibrarySuggestions(object):
    def setupUi(self, LibrarySuggestions):
        LibrarySuggestions.setObjectName(_fromUtf8("LibrarySuggestions"))
        LibrarySuggestions.resize(640, 480)
        LibrarySuggestions.buttonBox = QtGui.QDialogButtonBox(LibrarySuggestions)
        LibrarySuggestions.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        LibrarySuggestions.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        LibrarySuggestions.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        LibrarySuggestions.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        LibrarySuggestions.libsList = QtGui.QListView(LibrarySuggestions)
        LibrarySuggestions.libsList.setGeometry(QtCore.QRect(10, 50, 621, 381))
        LibrarySuggestions.libsList.setObjectName(_fromUtf8("libsList"))
        LibrarySuggestions.label = QtGui.QLabel(LibrarySuggestions)
        LibrarySuggestions.label.setGeometry(QtCore.QRect(20, 10, 601, 22))
        LibrarySuggestions.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(LibrarySuggestions)
        QtCore.QObject.connect(LibrarySuggestions.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LibrarySuggestions.accept)
        QtCore.QObject.connect(LibrarySuggestions.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LibrarySuggestions.reject)
        QtCore.QMetaObject.connectSlotsByName(LibrarySuggestions)

    def retranslateUi(self, LibrarySuggestions):
        LibrarySuggestions.setWindowTitle(_translate("LibrarySuggestions", "Library Suggestions", None))
        LibrarySuggestions.label.setText(_translate("LibrarySuggestions", "Undefined references found.  Consider the following dependencies:", None))


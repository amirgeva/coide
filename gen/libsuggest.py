# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/libsuggest.ui'
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

class Ui_LibrarySuggestions(object):
    def setupUi(self, LibrarySuggestions):
        LibrarySuggestions.setObjectName(_fromUtf8("LibrarySuggestions"))
        LibrarySuggestions.resize(640, 480)
        LibrarySuggestions.buttonBox = QtWidgets.QDialogButtonBox(LibrarySuggestions)
        LibrarySuggestions.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        LibrarySuggestions.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        LibrarySuggestions.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        LibrarySuggestions.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        LibrarySuggestions.libsList = QtWidgets.QListView(LibrarySuggestions)
        LibrarySuggestions.libsList.setGeometry(QtCore.QRect(10, 50, 621, 381))
        LibrarySuggestions.libsList.setObjectName(_fromUtf8("libsList"))
        LibrarySuggestions.label = QtWidgets.QLabel(LibrarySuggestions)
        LibrarySuggestions.label.setGeometry(QtCore.QRect(20, 10, 601, 22))
        LibrarySuggestions.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(LibrarySuggestions)
        LibrarySuggestions.buttonBox.accepted.connect(LibrarySuggestions.accept)
        LibrarySuggestions.buttonBox.rejected.connect(LibrarySuggestions.reject)
        QtCore.QMetaObject.connectSlotsByName(LibrarySuggestions)

    def retranslateUi(self, LibrarySuggestions):
        LibrarySuggestions.setWindowTitle(_translate("LibrarySuggestions", "Library Suggestions", None))
        LibrarySuggestions.label.setText(_translate("LibrarySuggestions", "Undefined references found.  Consider the following dependencies:", None))


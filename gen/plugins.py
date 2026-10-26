# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/plugins.ui'
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

class Ui_PluginsDialog(object):
    def setupUi(self, PluginsDialog):
        PluginsDialog.setObjectName(_fromUtf8("PluginsDialog"))
        PluginsDialog.resize(507, 359)
        PluginsDialog.buttonBox = QtWidgets.QDialogButtonBox(PluginsDialog)
        PluginsDialog.buttonBox.setGeometry(QtCore.QRect(140, 310, 341, 32))
        PluginsDialog.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        PluginsDialog.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        PluginsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        PluginsDialog.pluginsTable = QtWidgets.QTableWidget(PluginsDialog)
        PluginsDialog.pluginsTable.setGeometry(QtCore.QRect(10, 40, 491, 261))
        PluginsDialog.pluginsTable.setObjectName(_fromUtf8("pluginsTable"))
        PluginsDialog.pluginsTable.setColumnCount(0)
        PluginsDialog.pluginsTable.setRowCount(0)
        PluginsDialog.label = QtWidgets.QLabel(PluginsDialog)
        PluginsDialog.label.setGeometry(QtCore.QRect(10, 10, 121, 17))
        PluginsDialog.label.setObjectName(_fromUtf8("label"))
        PluginsDialog.pluginsDirectory = QtWidgets.QLineEdit(PluginsDialog)
        PluginsDialog.pluginsDirectory.setGeometry(QtCore.QRect(160, 10, 291, 27))
        PluginsDialog.pluginsDirectory.setObjectName(_fromUtf8("pluginsDirectory"))
        PluginsDialog.dirBrowse = QtWidgets.QPushButton(PluginsDialog)
        PluginsDialog.dirBrowse.setGeometry(QtCore.QRect(460, 10, 41, 27))
        PluginsDialog.dirBrowse.setObjectName(_fromUtf8("dirBrowse"))

        self.retranslateUi(PluginsDialog)
        PluginsDialog.buttonBox.accepted.connect(PluginsDialog.accept)
        PluginsDialog.buttonBox.rejected.connect(PluginsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginsDialog)

    def retranslateUi(self, PluginsDialog):
        PluginsDialog.setWindowTitle(_translate("PluginsDialog", "Plugins", None))
        PluginsDialog.label.setText(_translate("PluginsDialog", "Plugins Directory:", None))
        PluginsDialog.dirBrowse.setText(_translate("PluginsDialog", "...", None))


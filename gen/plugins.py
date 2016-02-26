# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/plugins.ui'
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

class Ui_PluginsDialog(object):
    def setupUi(self, PluginsDialog):
        PluginsDialog.setObjectName(_fromUtf8("PluginsDialog"))
        PluginsDialog.resize(507, 359)
        PluginsDialog.buttonBox = QtGui.QDialogButtonBox(PluginsDialog)
        PluginsDialog.buttonBox.setGeometry(QtCore.QRect(140, 310, 341, 32))
        PluginsDialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        PluginsDialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        PluginsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        PluginsDialog.pluginsTable = QtGui.QTableWidget(PluginsDialog)
        PluginsDialog.pluginsTable.setGeometry(QtCore.QRect(10, 40, 491, 261))
        PluginsDialog.pluginsTable.setObjectName(_fromUtf8("pluginsTable"))
        PluginsDialog.pluginsTable.setColumnCount(0)
        PluginsDialog.pluginsTable.setRowCount(0)
        PluginsDialog.label = QtGui.QLabel(PluginsDialog)
        PluginsDialog.label.setGeometry(QtCore.QRect(10, 10, 121, 17))
        PluginsDialog.label.setObjectName(_fromUtf8("label"))
        PluginsDialog.pluginsDirectory = QtGui.QLineEdit(PluginsDialog)
        PluginsDialog.pluginsDirectory.setGeometry(QtCore.QRect(160, 10, 291, 27))
        PluginsDialog.pluginsDirectory.setObjectName(_fromUtf8("pluginsDirectory"))
        PluginsDialog.dirBrowse = QtGui.QPushButton(PluginsDialog)
        PluginsDialog.dirBrowse.setGeometry(QtCore.QRect(460, 10, 41, 27))
        PluginsDialog.dirBrowse.setObjectName(_fromUtf8("dirBrowse"))

        self.retranslateUi(PluginsDialog)
        QtCore.QObject.connect(PluginsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PluginsDialog.accept)
        QtCore.QObject.connect(PluginsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PluginsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginsDialog)

    def retranslateUi(self, PluginsDialog):
        PluginsDialog.setWindowTitle(_translate("PluginsDialog", "Plugins", None))
        PluginsDialog.label.setText(_translate("PluginsDialog", "Plugins Directory:", None))
        PluginsDialog.dirBrowse.setText(_translate("PluginsDialog", "...", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/build_settings.ui'
#
# Created: Tue Sep 30 12:44:23 2014
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

class Ui_BuildSettingsDialog(object):
    def setupUi(self, BuildSettingsDialog):
        BuildSettingsDialog.setObjectName(_fromUtf8("BuildSettingsDialog"))
        BuildSettingsDialog.resize(464, 387)
        BuildSettingsDialog.buttonBox = QtGui.QDialogButtonBox(BuildSettingsDialog)
        BuildSettingsDialog.buttonBox.setGeometry(QtCore.QRect(110, 340, 341, 32))
        BuildSettingsDialog.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        BuildSettingsDialog.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        BuildSettingsDialog.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        BuildSettingsDialog.projTree = QtGui.QTreeWidget(BuildSettingsDialog)
        BuildSettingsDialog.projTree.setGeometry(QtCore.QRect(10, 10, 161, 321))
        BuildSettingsDialog.projTree.setHeaderHidden(True)
        BuildSettingsDialog.projTree.setObjectName(_fromUtf8("projTree"))
        BuildSettingsDialog.projTree.headerItem().setText(0, _fromUtf8("1"))
        BuildSettingsDialog.optCB = QtGui.QComboBox(BuildSettingsDialog)
        BuildSettingsDialog.optCB.setGeometry(QtCore.QRect(350, 10, 101, 27))
        BuildSettingsDialog.optCB.setObjectName(_fromUtf8("optCB"))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.label = QtGui.QLabel(BuildSettingsDialog)
        BuildSettingsDialog.label.setGeometry(QtCore.QRect(190, 10, 101, 20))
        BuildSettingsDialog.label.setObjectName(_fromUtf8("label"))
        BuildSettingsDialog.warnCB = QtGui.QComboBox(BuildSettingsDialog)
        BuildSettingsDialog.warnCB.setGeometry(QtCore.QRect(350, 50, 101, 27))
        BuildSettingsDialog.warnCB.setObjectName(_fromUtf8("warnCB"))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.label_2 = QtGui.QLabel(BuildSettingsDialog)
        BuildSettingsDialog.label_2.setGeometry(QtCore.QRect(190, 50, 81, 17))
        BuildSettingsDialog.label_2.setObjectName(_fromUtf8("label_2"))
        BuildSettingsDialog.pedantic = QtGui.QCheckBox(BuildSettingsDialog)
        BuildSettingsDialog.pedantic.setGeometry(QtCore.QRect(190, 80, 161, 22))
        BuildSettingsDialog.pedantic.setObjectName(_fromUtf8("pedantic"))
        BuildSettingsDialog.checkBox = QtGui.QCheckBox(BuildSettingsDialog)
        BuildSettingsDialog.checkBox.setGeometry(QtCore.QRect(190, 110, 201, 22))
        BuildSettingsDialog.checkBox.setObjectName(_fromUtf8("checkBox"))
        BuildSettingsDialog.customFlags = QtGui.QPlainTextEdit(BuildSettingsDialog)
        BuildSettingsDialog.customFlags.setGeometry(QtCore.QRect(180, 240, 271, 91))
        BuildSettingsDialog.customFlags.setObjectName(_fromUtf8("customFlags"))
        BuildSettingsDialog.label_3 = QtGui.QLabel(BuildSettingsDialog)
        BuildSettingsDialog.label_3.setGeometry(QtCore.QRect(180, 210, 191, 17))
        BuildSettingsDialog.label_3.setObjectName(_fromUtf8("label_3"))
        BuildSettingsDialog.resetButton = QtGui.QPushButton(BuildSettingsDialog)
        BuildSettingsDialog.resetButton.setGeometry(QtCore.QRect(320, 180, 131, 27))
        BuildSettingsDialog.resetButton.setObjectName(_fromUtf8("resetButton"))

        self.retranslateUi(BuildSettingsDialog)
        QtCore.QObject.connect(BuildSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), BuildSettingsDialog.accept)
        QtCore.QObject.connect(BuildSettingsDialog.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), BuildSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BuildSettingsDialog)

    def retranslateUi(self, BuildSettingsDialog):
        BuildSettingsDialog.setWindowTitle(_translate("BuildSettingsDialog", "Build Settings", None))
        BuildSettingsDialog.optCB.setItemText(0, _translate("BuildSettingsDialog", "-O2", None))
        BuildSettingsDialog.optCB.setItemText(1, _translate("BuildSettingsDialog", "-O0", None))
        BuildSettingsDialog.optCB.setItemText(2, _translate("BuildSettingsDialog", "-O1", None))
        BuildSettingsDialog.optCB.setItemText(3, _translate("BuildSettingsDialog", "-O3", None))
        BuildSettingsDialog.optCB.setItemText(4, _translate("BuildSettingsDialog", "Custom", None))
        BuildSettingsDialog.label.setText(_translate("BuildSettingsDialog", "Optimization", None))
        BuildSettingsDialog.warnCB.setItemText(0, _translate("BuildSettingsDialog", "Default", None))
        BuildSettingsDialog.warnCB.setItemText(1, _translate("BuildSettingsDialog", "None (-w)", None))
        BuildSettingsDialog.warnCB.setItemText(2, _translate("BuildSettingsDialog", "All (-Wall)", None))
        BuildSettingsDialog.label_2.setText(_translate("BuildSettingsDialog", "Warnings", None))
        BuildSettingsDialog.pedantic.setText(_translate("BuildSettingsDialog", "Pedantic", None))
        BuildSettingsDialog.checkBox.setText(_translate("BuildSettingsDialog", "Warnings as errors", None))
        BuildSettingsDialog.label_3.setText(_translate("BuildSettingsDialog", "Custom Flags", None))
        BuildSettingsDialog.resetButton.setText(_translate("BuildSettingsDialog", "Reset to Default", None))


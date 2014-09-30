# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/build_settings.ui'
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

class Ui_BuildSettingsDialog(object):
    def setupUi(self, BuildSettingsDialog):
        BuildSettingsDialog.setObjectName(_fromUtf8("BuildSettingsDialog"))
        BuildSettingsDialog.resize(464, 387)
        BuildSettingsDialog.projTree = QtGui.QTreeWidget(BuildSettingsDialog)
        BuildSettingsDialog.projTree.setGeometry(QtCore.QRect(10, 10, 161, 321))
        BuildSettingsDialog.projTree.setHeaderHidden(True)
        BuildSettingsDialog.projTree.setObjectName(_fromUtf8("projTree"))
        BuildSettingsDialog.projTree.headerItem().setText(0, _fromUtf8("1"))
        BuildSettingsDialog.label = QtGui.QLabel(BuildSettingsDialog)
        BuildSettingsDialog.label.setGeometry(QtCore.QRect(192, 48, 101, 20))
        BuildSettingsDialog.label.setObjectName(_fromUtf8("label"))
        BuildSettingsDialog.label_2 = QtGui.QLabel(BuildSettingsDialog)
        BuildSettingsDialog.label_2.setGeometry(QtCore.QRect(192, 80, 81, 17))
        BuildSettingsDialog.label_2.setObjectName(_fromUtf8("label_2"))
        BuildSettingsDialog.defaults = QtGui.QCheckBox(BuildSettingsDialog)
        BuildSettingsDialog.defaults.setGeometry(QtCore.QRect(192, 16, 151, 22))
        BuildSettingsDialog.defaults.setObjectName(_fromUtf8("defaults"))
        BuildSettingsDialog.settingsGroup = QtGui.QGroupBox(BuildSettingsDialog)
        BuildSettingsDialog.settingsGroup.setGeometry(QtCore.QRect(176, 32, 289, 305))
        BuildSettingsDialog.settingsGroup.setTitle(_fromUtf8(""))
        BuildSettingsDialog.settingsGroup.setObjectName(_fromUtf8("settingsGroup"))
        BuildSettingsDialog.optCB = QtGui.QComboBox(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.optCB.setGeometry(QtCore.QRect(176, 16, 101, 27))
        BuildSettingsDialog.optCB.setObjectName(_fromUtf8("optCB"))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.optCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.warnCB = QtGui.QComboBox(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.warnCB.setGeometry(QtCore.QRect(176, 48, 101, 27))
        BuildSettingsDialog.warnCB.setObjectName(_fromUtf8("warnCB"))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.warnCB.addItem(_fromUtf8(""))
        BuildSettingsDialog.pedantic = QtGui.QCheckBox(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.pedantic.setGeometry(QtCore.QRect(16, 80, 161, 22))
        BuildSettingsDialog.pedantic.setObjectName(_fromUtf8("pedantic"))
        BuildSettingsDialog.warnErrors = QtGui.QCheckBox(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.warnErrors.setGeometry(QtCore.QRect(16, 112, 201, 22))
        BuildSettingsDialog.warnErrors.setObjectName(_fromUtf8("warnErrors"))
        BuildSettingsDialog.customFlags = QtGui.QPlainTextEdit(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.customFlags.setGeometry(QtCore.QRect(16, 208, 257, 91))
        BuildSettingsDialog.customFlags.setObjectName(_fromUtf8("customFlags"))
        BuildSettingsDialog.label_3 = QtGui.QLabel(BuildSettingsDialog.settingsGroup)
        BuildSettingsDialog.label_3.setGeometry(QtCore.QRect(16, 176, 191, 17))
        BuildSettingsDialog.label_3.setObjectName(_fromUtf8("label_3"))
        BuildSettingsDialog.closeButton = QtGui.QPushButton(BuildSettingsDialog)
        BuildSettingsDialog.closeButton.setGeometry(QtCore.QRect(352, 352, 98, 27))
        BuildSettingsDialog.closeButton.setObjectName(_fromUtf8("closeButton"))

        self.retranslateUi(BuildSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(BuildSettingsDialog)

    def retranslateUi(self, BuildSettingsDialog):
        BuildSettingsDialog.setWindowTitle(_translate("BuildSettingsDialog", "Build Settings", None))
        BuildSettingsDialog.label.setText(_translate("BuildSettingsDialog", "Optimization", None))
        BuildSettingsDialog.label_2.setText(_translate("BuildSettingsDialog", "Warnings", None))
        BuildSettingsDialog.defaults.setText(_translate("BuildSettingsDialog", "Use Defaults", None))
        BuildSettingsDialog.optCB.setItemText(0, _translate("BuildSettingsDialog", "-O2", None))
        BuildSettingsDialog.optCB.setItemText(1, _translate("BuildSettingsDialog", "-O0", None))
        BuildSettingsDialog.optCB.setItemText(2, _translate("BuildSettingsDialog", "-O1", None))
        BuildSettingsDialog.optCB.setItemText(3, _translate("BuildSettingsDialog", "-O3", None))
        BuildSettingsDialog.optCB.setItemText(4, _translate("BuildSettingsDialog", "Custom", None))
        BuildSettingsDialog.warnCB.setItemText(0, _translate("BuildSettingsDialog", "Default", None))
        BuildSettingsDialog.warnCB.setItemText(1, _translate("BuildSettingsDialog", "None (-w)", None))
        BuildSettingsDialog.warnCB.setItemText(2, _translate("BuildSettingsDialog", "All (-Wall)", None))
        BuildSettingsDialog.pedantic.setText(_translate("BuildSettingsDialog", "Pedantic", None))
        BuildSettingsDialog.warnErrors.setText(_translate("BuildSettingsDialog", "Warnings as errors", None))
        BuildSettingsDialog.label_3.setText(_translate("BuildSettingsDialog", "Custom Flags", None))
        BuildSettingsDialog.closeButton.setText(_translate("BuildSettingsDialog", "Close", None))


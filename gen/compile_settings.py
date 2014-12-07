# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/compile_settings.ui'
#
#
#      by: PyQt4 UI code generator 4.11.2
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

class Ui_CompileSettings(object):
    def setupUi(self, CompileSettings):
        CompileSettings.setObjectName(_fromUtf8("CompileSettings"))
        CompileSettings.resize(400, 358)
        CompileSettings.label = QtGui.QLabel(CompileSettings)
        CompileSettings.label.setGeometry(QtCore.QRect(30, 60, 101, 20))
        CompileSettings.label.setObjectName(_fromUtf8("label"))
        CompileSettings.defaults = QtGui.QCheckBox(CompileSettings)
        CompileSettings.defaults.setGeometry(QtCore.QRect(16, 16, 151, 22))
        CompileSettings.defaults.setObjectName(_fromUtf8("defaults"))
        CompileSettings.label_2 = QtGui.QLabel(CompileSettings)
        CompileSettings.label_2.setGeometry(QtCore.QRect(30, 92, 81, 17))
        CompileSettings.label_2.setObjectName(_fromUtf8("label_2"))
        CompileSettings.settingsGroup = QtGui.QGroupBox(CompileSettings)
        CompileSettings.settingsGroup.setGeometry(QtCore.QRect(14, 42, 289, 305))
        CompileSettings.settingsGroup.setTitle(_fromUtf8(""))
        CompileSettings.settingsGroup.setObjectName(_fromUtf8("settingsGroup"))
        CompileSettings.optCB = QtGui.QComboBox(CompileSettings.settingsGroup)
        CompileSettings.optCB.setGeometry(QtCore.QRect(176, 16, 101, 27))
        CompileSettings.optCB.setObjectName(_fromUtf8("optCB"))
        CompileSettings.optCB.addItem(_fromUtf8(""))
        CompileSettings.optCB.addItem(_fromUtf8(""))
        CompileSettings.optCB.addItem(_fromUtf8(""))
        CompileSettings.optCB.addItem(_fromUtf8(""))
        CompileSettings.optCB.addItem(_fromUtf8(""))
        CompileSettings.warnCB = QtGui.QComboBox(CompileSettings.settingsGroup)
        CompileSettings.warnCB.setGeometry(QtCore.QRect(176, 48, 101, 27))
        CompileSettings.warnCB.setObjectName(_fromUtf8("warnCB"))
        CompileSettings.warnCB.addItem(_fromUtf8(""))
        CompileSettings.warnCB.addItem(_fromUtf8(""))
        CompileSettings.warnCB.addItem(_fromUtf8(""))
        CompileSettings.pedantic = QtGui.QCheckBox(CompileSettings.settingsGroup)
        CompileSettings.pedantic.setGeometry(QtCore.QRect(20, 80, 161, 22))
        CompileSettings.pedantic.setObjectName(_fromUtf8("pedantic"))
        CompileSettings.warnErrors = QtGui.QCheckBox(CompileSettings.settingsGroup)
        CompileSettings.warnErrors.setGeometry(QtCore.QRect(20, 110, 201, 22))
        CompileSettings.warnErrors.setObjectName(_fromUtf8("warnErrors"))
        CompileSettings.customFlags = QtGui.QPlainTextEdit(CompileSettings.settingsGroup)
        CompileSettings.customFlags.setGeometry(QtCore.QRect(16, 200, 261, 91))
        CompileSettings.customFlags.setObjectName(_fromUtf8("customFlags"))
        CompileSettings.label_3 = QtGui.QLabel(CompileSettings.settingsGroup)
        CompileSettings.label_3.setGeometry(QtCore.QRect(16, 176, 191, 17))
        CompileSettings.label_3.setObjectName(_fromUtf8("label_3"))
        CompileSettings.cpp11 = QtGui.QCheckBox(CompileSettings.settingsGroup)
        CompileSettings.cpp11.setGeometry(QtCore.QRect(20, 140, 115, 27))
        CompileSettings.cpp11.setObjectName(_fromUtf8("cpp11"))

        self.retranslateUi(CompileSettings)
        QtCore.QMetaObject.connectSlotsByName(CompileSettings)

    def retranslateUi(self, CompileSettings):
        CompileSettings.setWindowTitle(_translate("CompileSettings", "Dialog", None))
        CompileSettings.label.setText(_translate("CompileSettings", "Optimization", None))
        CompileSettings.defaults.setText(_translate("CompileSettings", "Use Defaults", None))
        CompileSettings.label_2.setText(_translate("CompileSettings", "Warnings", None))
        CompileSettings.optCB.setItemText(0, _translate("CompileSettings", "-O2", None))
        CompileSettings.optCB.setItemText(1, _translate("CompileSettings", "-O0", None))
        CompileSettings.optCB.setItemText(2, _translate("CompileSettings", "-O1", None))
        CompileSettings.optCB.setItemText(3, _translate("CompileSettings", "-O3", None))
        CompileSettings.optCB.setItemText(4, _translate("CompileSettings", "Custom", None))
        CompileSettings.warnCB.setItemText(0, _translate("CompileSettings", "Default", None))
        CompileSettings.warnCB.setItemText(1, _translate("CompileSettings", "None (-w)", None))
        CompileSettings.warnCB.setItemText(2, _translate("CompileSettings", "All (-Wall)", None))
        CompileSettings.pedantic.setText(_translate("CompileSettings", "Pedantic", None))
        CompileSettings.warnErrors.setText(_translate("CompileSettings", "Warnings as errors", None))
        CompileSettings.label_3.setText(_translate("CompileSettings", "Custom Flags", None))
        CompileSettings.cpp11.setText(_translate("CompileSettings", "C++ 11", None))


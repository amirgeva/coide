from PyQt6 import QtGui
from PyQt6 import QtWidgets


class PluginCursor(QtGui.QTextCursor):
    def __init__(self,*args):
        super(PluginCursor,self).__init__(*args)



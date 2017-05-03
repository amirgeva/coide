from PyQt4 import QtGui


class PluginCursor(QtGui.QTextCursor):
    def __init__(self,*args):
        super(PluginCursor,self).__init__(*args)



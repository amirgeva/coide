from PyQt4 import QtCore
from PyQt4 import QtGui
import uis
from consts import *


class BuildSettingsDialog(QtGui.QDialog):
    def __init__(self,mainwin,parent=None):
        super(BuildSettingsDialog,self).__init__(parent)
        self.mainWindow=mainwin
        uis.loadDialog('build_settings',self)
        self.globalItem=QtGui.QTreeWidgetItem(['Global'])
        self.projTree.addTopLevelItem(self.globalItem)
        self.workspaceItem=QtGui.QTreeWidgetItem(['Workspace'])
        self.mainWindow.workspaceTree.addProjectsToTree(self.workspaceItem)
        self.globalItem.addChild(self.workspaceItem)
        self.projTree.itemSelectionChanged.connect(self.selectionChanged)
        
    def selectionChanged(self):
        print self.projTree.currentItem().data(0,DirectoryRole).toString()
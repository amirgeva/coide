from PyQt4 import QtCore
from PyQt4 import QtGui
import os
import uis
from consts import *
from properties import Properties

def buildName(name):
    return 'BUILD_'+name

def getBool(props,name,default):
    if not props.has(buildName(name)):
        return default
    return (props.get(buildName(name))=='True')

def setBool(props,name,value):
    props.assign(buildName(name),'True' if value else 'False')

def getStr(props,name,default):
    value=props.get(buildName(name),default)
    value=value.replace('\\n','\n')
    return value

def setStr(props,name,value):
    lines=value.split('\n')
    value='\\n'.join(lines)
    props.assign(buildName(name),value)
        
def check(checkbox,boolState):
    state = QtCore.Qt.Checked if boolState else QtCore.Qt.Unchecked
    checkbox.setCheckState(state)
    return boolState
    
def getCheck(checkbox):
    return (checkbox.checkState() == QtCore.Qt.Checked)
    
def setCombo(cb,value):
    n=cb.count()
    for i in xrange(0,n):
        if cb.itemText(i)==value:
            cb.setCurrentIndex(i)
            return
                
class BuildSettingsDialog(QtGui.QDialog):
    def __init__(self,mainwin,startPath,parent=None):
        super(BuildSettingsDialog,self).__init__(parent)
        self.mainWindow=mainwin
        uis.loadDialog('build_settings',self)
        self.settingsGroup.setDisabled(True)
        self.defaults.stateChanged.connect(self.defaultsToggled)
        self.workspaceItem=QtGui.QTreeWidgetItem(['Workspace'])
        self.mainWindow.workspaceTree.addProjectsToTree(self.workspaceItem)
        self.workspaceDir=self.workspaceItem.data(0,DirectoryRole).toString()
        self.projTree.addTopLevelItem(self.workspaceItem)
        self.workspaceItem.setExpanded(True)
        self.projTree.itemSelectionChanged.connect(self.selectionChanged)
        self.closeButton.clicked.connect(self.closeClicked)
        self.prevPath=''
        firstItem=None
        if startPath==self.workspaceDir:
            firstItem=self.workspaceItem
        else:
            firstItem=self.findItem(self.workspaceItem,startPath)
        if not firstItem:
            firstItem=self.workspaceItem
        self.projTree.setCurrentItem(firstItem)
        self.projTree.scrollToItem(firstItem)
        dir=firstItem.data(0,DirectoryRole).toString()
        self.prevPath=os.path.join(dir,'mk.cfg')
        
    def findItem(self,parent,path):
        n=parent.childCount()
        for i in xrange(0,n):
            item=parent.child(i)
            dir=item.data(0,DirectoryRole).toString()
            if dir==path:
                return item
            res=self.findItem(item,path)
            if res:
                return res
        return None
        
    def closeClicked(self):
        self.save(self.prevPath)
        self.close()
        
    def defaultsToggled(self,state):
        if state==QtCore.Qt.Checked:
            self.settingsGroup.setDisabled(True)
        else:
            self.settingsGroup.setEnabled(True)
        
    def selectionChanged(self):
        if self.prevPath:
            self.save(self.prevPath)
        item=self.projTree.currentItem()
        dir=item.data(0,DirectoryRole).toString()
        path=os.path.join(dir,'mk.cfg')
        self.load(path)
        self.prevPath=path
        
    def load(self,path):
        props=Properties(path)
        if check(self.defaults,getBool(props,'DEFAULTS',True)):
            self.settingsGroup.setDisabled(True)
        else:
            self.settingsGroup.setEnabled(True)
        setCombo(self.optCB,getStr(props,'OPT','-O2'))
        setCombo(self.warnCB,getStr(props,'WARN','Default'))
        check(self.pedantic,getBool(props,'PEDANTIC',False))
        check(self.warnErrors,getBool(props,'WARNERR',False))
        self.customFlags.setPlainText(getStr(props,'CUSTOM',''))
        
    def save(self,path):
        props=Properties(path)
        setBool(props,'DEFAULTS',getCheck(self.defaults))
        setStr(props,'OPT',self.optCB.currentText())
        setStr(props,'WARN',self.warnCB.currentText())
        setBool(props,'PEDANTIC',getCheck(self.pedantic))
        setBool(props,'WARNERR',getCheck(self.warnErrors))
        setStr(props,'CUSTOM',self.customFlags.toPlainText())
        props.save(path)
        

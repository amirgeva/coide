from PyQt4 import QtCore
from PyQt4 import QtGui
import os
import uis
from build_settings_cfg import tabs
from consts import DirectoryRole
from properties import Properties

def getBool(props,name,default):
    if not props.has(name):
        return default
    return (props.get(name)=='True')

def setBool(props,name,value):
    props.assign(name,'True' if value else 'False')

def getStr(props,name,default):
    value=props.get(name,default)
    value=value.replace('\\n','\n')
    return value

def setStr(props,name,value):
    lines=value.split('\n')
    value='\\n'.join(lines)
    props.assign(name,value)
        
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

def load(widget,value):
    t=type(widget).__name__
    if t=='QLineEdit':
        widget.setText(value)
    if t=='QPlainTextEdit':
        widget.setPlainText(value.replace('\\n','\n'))
    if t=='QCheckBox':
        check(widget,value=='True')
    if t=='QComboBox':
        setCombo(widget,value)

def save(widget):
    t=type(widget).__name__
    if t=='QLineEdit':
        return widget.text()
    if t=='QPlainTextEdit':
        return widget.toPlainText().replace('\n','\\n')
    if t=='QCheckBox':
        return getCheck(widget)
    if t=='QComboBox':
        return widget.itemText(widget.currentIndex())

class SettingsTabDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(SettingsTabDialog,self).__init__(parent)
        # fields maps setting name to widget
        self.fields={}
        
    def addWidgets(self,desc):
        '''
        Add widgets based on the description in desc
        which is a list of tuples describing individual widgets
        '''
        layout=QtGui.QGridLayout()
        row=0
        for d in desc:
            n=len(d)
            name=d[0]
            title=d[1]
            details=d[2]
            layout.addWidget(QtGui.QLabel(title),row,0)
            w=None
            if details=='STR':
                w=QtGui.QLineEdit()
                w.setText(d[3])
            if details=='EDIT':
                w=QtGui.QPlainTextEdit()
                w.setPlainText(d[3].replace('\\n','\n'))
            if details=='CB':
                w=QtGui.QCheckBox()
                check(w,d[3])
            if '|' in details:
                w=QtGui.QComboBox()
                opts=details.split('|')
                for o in opts:
                    w.addItem(o)
                setCombo(w,d[3])
            if (w):
                self.fields[name]=w
                layout.addWidget(w,row,1)
            row=row+1
        self.setLayout(layout)
        
    def load(self,props):
        for name in self.fields:
            w=self.fields.get(name)
            if props.has(name):
                load(w,props.get(name))
    
    def save(self,props):
        for name in self.fields:
            w=self.fields.get(name)
            props.assign(name,save(w))
            
                
class BuildSettingsDialog(QtGui.QDialog):
    def __init__(self,mainwin,startPath,parent=None):
        super(BuildSettingsDialog,self).__init__(parent)
        self.mainWindow=mainwin
        uis.loadDialog('build_settings',self)
        s=QtCore.QSettings()
        check(self.parallelCB,s.value('parallel_make',False).toBool())
        check(self.symscanCB,s.value('symbol_scan',True).toBool())
        self.tabWidget.clear()
        self.tabs=[]
        for t in tabs:
            desc=tabs.get(t)
            dlg=SettingsTabDialog()
            dlg.addWidgets(desc)
            self.tabs.append((t,dlg))
        for (name,tab) in self.tabs:
            self.tabWidget.addTab(tab,name)
        self.workspaceItem=QtGui.QTreeWidgetItem(['Workspace'])
        self.mainWindow.workspaceTree.addProjectsToTree(self.workspaceItem)
        self.workspaceDir=self.workspaceItem.data(0,DirectoryRole).toString()
        self.projTree.addTopLevelItem(self.workspaceItem)
        self.workspaceItem.setExpanded(True)
        self.projTree.itemSelectionChanged.connect(self.selectionChanged)
        self.closeButton.clicked.connect(self.closeClicked)
        self.resetButton.clicked.connect(self.resetClicked)
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
        s=QtCore.QSettings()
        s.setValue('parallel_make',getCheck(self.parallelCB))
        s.setValue('symbol_scan',getCheck(self.symscanCB))
        s.sync()
        self.close()
        
    def resetClicked(self):
        res=QtGui.QMessageBox.question(self,'Delete File','Delete '+self.prevPath,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if res==QtGui.QMessageBox.Yes:
            try:
                os.remove(self.prevPath)
            except OSError:
                pass
        
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
        for (name,tab) in self.tabs:
            tab.load(props)
        
    def save(self,path):
        props=Properties(path)
        for (name,tab) in self.tabs:
            tab.save(props)
        props.save(path)
        

if __name__=='__main__':
    import sys
    from build_settings_cfg import tabs
    app=QtGui.QApplication(sys.argv)
    d=SettingsTabDialog()
    d.addWidgets(tabs.get('Compile'))
    d.show()
    app.exec_()
    
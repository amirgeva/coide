import os
import re
from PyQt4 import QtCore
from PyQt4 import QtGui
from consts import *
from properties import Properties
from depsdlg import DependenciesDialog
import utils

class WorkSpace(QtGui.QTreeWidget):

    depsChanged=QtCore.pyqtSignal()    
    
    def __init__(self,pane,mainwin):
        super(WorkSpace,self).__init__(pane)
        self.mainWindow=mainwin
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setMainAction = QtGui.QAction('Set Main Project',self,triggered=self.setMain)        
        self.editDependenciesAction = QtGui.QAction('Dependencies',self,triggered=self.editDependencies)
        self.main=None
        s=QtCore.QSettings()
        self.root=s.value('workspace').toString()
        
    def contextMenuEvent(self,event):
        menu=QtGui.QMenu()
        dirpath=self.currentItem().data(0,DirectoryRole).toString()
        if len(dirpath)>0:
            makefile=os.path.join(dirpath,"Makefile")
            if os.path.exists(makefile):
                menu.addAction(self.setMainAction)
                menu.addAction(self.editDependenciesAction)
        menu.exec_(event.globalPos())
        
    def findDirectoryItem(self,path,parent=None):
        if not parent:
            n=self.topLevelItemCount()
            for i in xrange(0,n):
                item=self.topLevelItem(i)
                res=self.findDirectoryItem(path,item)
                if res:
                    return res
        else:
            dirpath=parent.data(0,DirectoryRole).toString()
            if dirpath==path:
                return parent
            n=parent.childCount()
            for i in xrange(0,n):
                item=parent.child(i)
                res=self.findDirectoryItem(path,item)
                if res:
                    return res
        return None
        
    def loadSettings(self):
        settings=QtCore.QSettings()
        mainpath=settings.value('mainproj').toString()
        self.setMainItem(self.findDirectoryItem(mainpath),save=False)
        
    def mainPath(self):        
        if self.main:
            return self.main.data(0,DirectoryRole).toString()
        return ""

    def editDependencies(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        mkPath=os.path.join(path,"mk.cfg")
        props=Properties(mkPath)
        libs=re.split('\W+',props.get('LIBS'))
        d=DependenciesDialog(libs)
        if d.exec_():
            props.assign("LIBS",",".join(d.libs))
            props.save(mkPath)
            self.depsChanged.emit()
            return True
        return False
        
        
    def setMain(self):
        self.setMainItem(self.currentItem())
        
    def setMainItem(self,item,save=True):
        if self.main:
            font=QtGui.QFont(self.main.font(0))
            font.setBold(False)
            self.main.setFont(0,font)        
        if item:
            font=QtGui.QFont(item.font(0))
            font.setBold(True)
            item.setFont(0,font)
            self.scrollToItem(item)
            self.expandItem(item)
        self.main=item
        if save:
            settings=QtCore.QSettings()
            settings.setValue('mainproj',self.main.data(0,DirectoryRole).toString())
            settings.sync()
        
        
    def update(self):
        self.clear()
        folderIcon=utils.loadIcon('folder')
        docIcon=utils.loadIcon('doc')

        if not os.path.exists(self.root):
            return
        items={}
        for (dir,subdirs,files) in os.walk(self.root):
            #dir=dir[2:]
            if dir and not dir[0]=='.':
                if not dir in items:
                    topItem=QtGui.QTreeWidgetItem([dir])
                    topItem.setIcon(0,folderIcon)
                    topItem.setData(0,DirectoryRole,dir)
                    items[dir]=topItem
                    self.addTopLevelItem(topItem)
                item=items.get(dir)
                for sub in subdirs:
                    path=os.path.join(dir,sub)
                    child=QtGui.QTreeWidgetItem([sub])
                    child.setIcon(0,folderIcon)
                    child.setData(0,DirectoryRole,path)
                    items[path]=child
                    item.addChild(child)
                for filename in files:
                    if filename.endswith('.cpp') or filename.endswith('.h'):
                        child=QtGui.QTreeWidgetItem([filename])
                        child.setIcon(0,docIcon)
                        item.addChild(child)
                        child.setData(0,FileRole,os.path.join(dir,filename))
        self.loadSettings()
    
    def setWorkspacePath(self,path):
        self.root=path
        s=QtCore.QSettings()
        s.setValue('workspace',path)
        s.sync()
        self.update()
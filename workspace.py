import os
import re
from PyQt4 import QtCore
from PyQt4 import QtGui
from consts import *
from properties import Properties
from depsdlg import DependenciesDialog
import utils
import uis

class WorkSpace(QtGui.QTreeWidget):

    depsChanged=QtCore.pyqtSignal()    
    
    def __init__(self,pane,mainwin):
        super(WorkSpace,self).__init__(pane)
        self.mainWindow=mainwin
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.actBuild = QtGui.QAction('Build',self,triggered=self.buildCurrent)
        self.actRebuild = QtGui.QAction('Rebuild',self,triggered=self.rebuildCurrent)
        self.actSetMain = QtGui.QAction('Set Main Project',self,triggered=self.setMain)        
        self.actEditDependencies = QtGui.QAction('Dependencies',self,triggered=self.editDependencies)
        self.actDebugSettings = QtGui.QAction('Debug Settings',self,triggered=self.editDebugSettings)
        self.actCreateFolder = QtGui.QAction('Create Folder',self,triggered=self.createFolder)
        self.actCreateFile = QtGui.QAction('Create File',self,triggered=self.createFile)
        self.main=None
        self.debug=('','')
        s=QtCore.QSettings()
        self.root=s.value('workspace').toString()
        self.config="Debug"
        
    def setConfig(self,config):
        self.config=config
        
    def contextMenuEvent(self,event):
        menu=QtGui.QMenu()
        dirpath=self.currentItem().data(0,DirectoryRole).toString()
        if len(dirpath)>0:
            makefile=os.path.join(dirpath,"Makefile")
            if os.path.exists(makefile):
                menu.addAction(self.actBuild)
                menu.addAction(self.actRebuild)
                menu.addSeparator()
                menu.addAction(self.actSetMain)
                menu.addAction(self.actEditDependencies)
                menu.addAction(self.actDebugSettings)
                menu.addSeparator()
            menu.addAction(self.actCreateFolder)
            menu.addAction(self.actCreateFile)
        if menu:
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
        self.setMainPath(mainpath)
        
    def loadMainProjectInfo(self):
        mkPath=os.path.join(self.mainPath(),"mk.cfg")
        props=Properties(mkPath)
        self.debug=(props.get("CWD"),props.get("PARAMS"))
        
    def mainPath(self):        
        if self.main:
            return self.main.data(0,DirectoryRole).toString()
        return ""

    def buildCurrent(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.buildSpecific(path)

    def rebuildCurrent(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.cleanSpecific(path)
        self.mainWindow.buildSpecific(path)

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
        
    def addLibrariesToProject(self,libs):
        if self.main:
            path=self.mainPath()
            mkPath=os.path.join(path,"mk.cfg")
            props=Properties(mkPath)
            lst=props.get("LIBS").split(',')
            lst=[x for x in lst if len(x)>0]
            for l in libs:
                lst.append(l)
            props.assign("LIBS",",".join(lst))
            props.save(mkPath)
            self.depsChanged.emit()
        
    def editDebugSettings(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        mkPath=os.path.join(path,"mk.cfg")
        props=Properties(mkPath)
        d=uis.loadDialog('debug_settings')
        d.cwdEdit.setText(props.get("CWD"))
        d.paramsEdit.setText(props.get("PARAMS"))
        if d.exec_():
            props.assign('CWD',d.cwdEdit.text())
            props.assign('PARAMS',d.paramsEdit.text())
            self.debug=(d.cwdEdit.text(),d.paramsEdit.text())
            props.save(mkPath)
            
    def createFolder(self):
        (name,rc)=QtGui.QInputDialog.getText(self,"Create Folder","Folder Name")
        if rc:
            item=self.currentItem()
            path=item.data(0,DirectoryRole).toString()
            try:
                os.mkdir(os.path.join(path,name))
                self.update()
            except OSError,e:
                utils.message("Failed to create folder")
        
    def createFile(self):
        (name,rc)=QtGui.QInputDialog.getText(self,"Create File","File Name")
        if rc:
            item=self.currentItem()
            path=item.data(0,DirectoryRole).toString()
            try:
                f=open(os.path.join(path,name),"w")
                f.write("\n")
                f.close()
                self.update()
            except IOError,e:
                utils.message("Failed to create file")
        

    def getDebugDirectory(self):
        return self.debug[0]
        
    def getDebugParams(self):
        return self.debug[1]

    def getExecutablePath(self):
        mkPath=os.path.join(self.mainPath(),"Makefile")
        outPath=utils.findLine(mkPath,"OUTPUT_PATH_{}=".format(self.config),True)
        return outPath

        
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
        self.loadMainProjectInfo()
        if save:
            settings=QtCore.QSettings()
            settings.setValue('mainproj',self.main.data(0,DirectoryRole).toString())
            settings.sync()
            
    def setMainPath(self,mainpath):
        mainitem=self.findDirectoryItem(mainpath)
        self.setMainItem(mainitem,save=False)
        self.loadMainProjectInfo()
        
    def update(self):
        self.main=None
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
import os
import re
import shutil
from PyQt4 import QtCore
from PyQt4 import QtGui
from consts import DirectoryRole,FileRole
from properties import Properties
from depsdlg import DependenciesDialog
from globals import is_src_ext, is_header
import utils
import uis

class WorkSpace(QtGui.QTreeWidget):

    depsChanged=QtCore.pyqtSignal(str)
    
    def __init__(self,pane,mainwin):
        super(WorkSpace,self).__init__(pane)
        self.mainWindow=mainwin
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.actBuild = QtGui.QAction('Build',self,triggered=self.buildCurrent)
        self.actClean = QtGui.QAction('Clean',self,triggered=self.cleanCurrent)
        self.actRebuild = QtGui.QAction('Rebuild',self,triggered=self.rebuildCurrent)
        self.actBuildSettings = QtGui.QAction('Build Settings',self,triggered=self.buildSettings)
        self.actCopySettings = QtGui.QAction('Copy Settings',self,triggered=self.copySettings)
        self.actSetMain = QtGui.QAction('Set Main Project',self,triggered=self.setMain)        
        self.actEditDependencies = QtGui.QAction('Dependencies',self,triggered=self.editDependencies)
        self.actDebugSettings = QtGui.QAction('Debug Settings',self,triggered=self.editDebugSettings)
        self.actGenerate = QtGui.QAction('Generate Makefile',self,triggered=self.generate)
        self.actCreateFolder = QtGui.QAction('Create Folder',self,triggered=self.createFolder)
        self.actCreateHWFolder = QtGui.QAction('Create App Project',self,triggered=self.createAppProject)
        self.actCreateFile = QtGui.QAction('Create File',self,triggered=self.createFile)
        self.actRefresh = QtGui.QAction('Refresh',self,triggered=self.refreshWorkspace)
        self.actDelete = QtGui.QAction('Delete',self,triggered=self.deletePath)
        self.actRename = QtGui.QAction('Rename',self,triggered=self.renamePath)
        self.actSCMDiff = QtGui.QAction('SCM Diff',self,triggered=self.scmDiffPath)
        self.main=None
        self.src=None
        self.debug=('','')
        s=QtCore.QSettings()
        self.sorting=s.value('sortFiles',True).toBool()
        self.root=s.value('workspace').toString()
        self.wsini=os.path.join(self.root,'settings.ini')
        self.config="Debug"
        self.fileItems={}
        self.itemCollapsed.connect(self.onCollapsed)
        self.itemExpanded.connect(self.onExpanded)
        
    def openFile(self,path):
        self.mainWindow.openSourceFile(path)
        
    def exists(self,filename):
        def fileExists(root,filename):
            if root.text(0)==filename:
                return root.data(0,FileRole).toString()
            for i in xrange(0,root.childCount()):
                res=fileExists(root.child(i),filename)
                if res:
                    return res
            return None
        for i in xrange(0,self.topLevelItemCount()):
            res=fileExists(self.topLevelItem(i),filename)
            if res:
                return res
        return None
        
    def setSorting(self,sorting):
        self.sorting=sorting
        # apply sort

    def onClose(self):
        self.saveSettings()
        
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
                menu.addAction(self.actClean)
                menu.addAction(self.actBuildSettings)
                menu.addAction(self.actCopySettings)
                menu.addSeparator()
                menu.addAction(self.actSetMain)
                menu.addAction(self.actEditDependencies)
                menu.addAction(self.actDebugSettings)
                menu.addSeparator()
            else:
                if dirpath==self.root:
                    menu.addAction(self.actBuildSettings)
            menu.addAction(self.actGenerate)
            menu.addAction(self.actCreateFolder)
            menu.addAction(self.actCreateHWFolder)
            menu.addAction(self.actCreateFile)
            menu.addAction(self.actRefresh)
        else:
            filepath=self.currentItem().data(0,FileRole).toString()
            if os.path.isfile(filepath):
                menu.addAction(self.actRename)
                menu.addAction(self.actDelete)
                menu.addAction(self.actSCMDiff)
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
        
    def getExpandedChildPaths(self,parent):
        res=[]
        for i in xrange(0,parent.childCount()):
            item=parent.child(i)
            dir=item.data(0,DirectoryRole).toString()
            if dir and self.isItemExpanded(item):
                res.append(dir)
            res=res+self.getExpandedChildPaths(item)
        return res
        
    def getExpandedPaths(self):
        res=[]
        for i in xrange(0,self.topLevelItemCount):
            item=self.topLevelItem(i)
            dir=item.data(0,DirectoryRole).toString()
            if dir and self.isItemExpanded(item):
                res.append(dir)
            res=res+self.getExpandedChildPaths(item)
        return res
        
    def settings(self):
        return QtCore.QSettings(self.wsini,QtCore.QSettings.IniFormat)
        
    def loadSettings(self):
        settings=self.settings()
        mainpath=settings.value('mainproj').toString()
        self.setMainPath(mainpath)
        e=set(settings.value('expanded').toString().split(','))
        for dir in e:
            item=self.findDirectoryItem(dir)
            if item:
                self.expandItem(item)
        self.loadBreakpoints()
        
    def saveSettings(self):
        self.saveBreakpoints()
        settings=self.settings()
        if self.main:
            settings.setValue('mainproj',self.main.data(0,DirectoryRole).toString())
        settings.sync()
        
    def onCollapsed(self,item):
        s=self.settings()
        e=set(s.value('expanded').toString().split(','))
        e.remove(item.data(0,DirectoryRole).toString())
        s.setValue('expanded',','.join(e))
        s.sync()
    
    def onExpanded(self,item):
        s=self.settings()
        e=set(s.value('expanded').toString().split(','))
        e.add(item.data(0,DirectoryRole).toString())
        s.setValue('expanded',','.join(e))
        s.sync()
        
    def loadMainProjectInfo(self):
        mkPath=os.path.join(self.mainPath(),"mk.cfg")
        props=Properties(mkPath)
        self.debug=(props.get("DEBUG_CWD"),props.get("DEBUG_PARAMS"))
        
    def mainPath(self):        
        if self.main:
            return self.main.data(0,DirectoryRole).toString()
        return ""
        
    def generate(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.generateQueue.add(path)
        
    def buildSettings(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.buildSettings(path)
        
    def copySettings(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        src=QtGui.QFileDialog.getExistingDirectory(caption="Copy From",directory=path)
        if src:
            shutil.copy(os.path.join(src,'mk.cfg'),path)
            self.mainWindow.generateQueue.add(path)
        
    def buildCurrent(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.buildSpecific(path)
        
    def cleanCurrent(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.cleanSpecific(path)

    def rebuildCurrent(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        self.mainWindow.rebuildSpecific(path)

    def editDependencies(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        mkPath=os.path.join(path,"mk.cfg")
        props=Properties(mkPath)
        libs=re.split('\W+',props.get('LINK_LIBS'))
        d=DependenciesDialog(libs)
        if d.exec_():
            props.assign("LINK_LIBS",",".join(d.libs))
            props.save(mkPath)
            self.depsChanged.emit(path)
            return True
        return False
        
    def getCurrentItemPath(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        if len(path)==0:
            path=item.data(0,FileRole).toString()
        return path
        
    def scmDiffPath(self):
        import scm
        path=self.getCurrentItemPath()
        scm.diff(self.root,path)
        
    def renamePath(self):
        oldpath=self.getCurrentItemPath()
        (name,rc)=QtGui.QInputDialog.getText(self,"Rename","New Name")
        newpath=os.path.dirname(oldpath)
        newpath=os.path.join(newpath,name)
        os.rename(oldpath,newpath)
        self.refreshWorkspace()
        
    def deletePath(self):
        path=self.getCurrentItemPath()
        res=QtGui.QMessageBox.question(self,'Delete File','Are you sure?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if res==QtGui.QMessageBox.Yes:
            try:
                os.remove(path)
                self.refreshWorkspace()
            except OSError:
                pass
        
    def addLibrariesToProject(self,libs):
        if self.main:
            path=self.mainPath()
            mkPath=os.path.join(path,"mk.cfg")
            props=Properties(mkPath)
            lst=props.get("LINK_LIBS").split(',')
            lst=[x for x in lst if len(x)>0]
            for l in libs:
                lst.append(l)
            props.assign("LINK_LIBS",",".join(lst))
            props.save(mkPath)
            self.depsChanged.emit(path)
        
    def editDebugSettings(self):
        item=self.currentItem()
        path=item.data(0,DirectoryRole).toString()
        mkPath=os.path.join(path,"mk.cfg")
        props=Properties(mkPath)
        d=uis.loadDialog('debug_settings')
        d.cwdEdit.setText(props.get("DEBUG_CWD"))
        d.paramsEdit.setText(props.get("DEBUG_PARAMS"))
        d.browseDirButton.clicked.connect(lambda: utils.browseDirectory(d.cwdEdit))
        if d.exec_():
            props.assign('DEBUG_CWD',d.cwdEdit.text())
            props.assign('DEBUG_PARAMS',d.paramsEdit.text())
            self.debug=(d.cwdEdit.text(),d.paramsEdit.text())
            props.save(mkPath)
            
    def createFolder(self):
        (name,rc)=QtGui.QInputDialog.getText(self,"Create Folder","Folder Name")
        if rc:
            item=self.currentItem()
            path=item.data(0,DirectoryRole).toString()
            try:
                path=os.path.join(path,name)
                os.mkdir(path)
                self.update()
                return path
            except OSError:
                utils.message("Failed to create folder")
        return ''
                
    def createAppProject(self):
        path=self.createFolder()
        if len(path)>0:
            self.mainWindow.createHelloWorldProject(path)
        
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
            except IOError:
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
            settings=self.settings()
            settings.setValue('mainproj',self.main.data(0,DirectoryRole).toString())
            settings.sync()
            
    def setMainPath(self,mainpath):
        if mainpath and len(mainpath)>0:
            #print "Setting main path to: '{}'".format(mainpath)
            mainitem=self.findDirectoryItem(mainpath)
            self.setMainItem(mainitem,save=False)
            self.loadMainProjectInfo()

    def refreshWorkspace(self):
        self.update()
        
    def scanDirectory(self,subroot):
        items={}
        for (dir,subdirs,files) in os.walk(os.path.join(self.root,subroot)):
            if dir and not dir[0]=='.':
                if not dir in items:
                    topItem=QtGui.QTreeWidgetItem([subroot])
                    if subroot=='src':
                        self.src=topItem
                    topItem.setIcon(0,self.folderIcon)
                    topItem.setData(0,DirectoryRole,dir)
                    items[dir]=topItem
                    self.rootItem.addChild(topItem)
                item=items.get(dir)
                for sub in subdirs:
                    path=os.path.join(dir,sub)
                    child=QtGui.QTreeWidgetItem([sub])
                    child.setIcon(0,self.folderIcon)
                    child.setData(0,DirectoryRole,path)
                    items[path]=child
                    item.addChild(child)
                for filename in files:
                    if is_src_ext(filename) or is_header(filename):
                        child=QtGui.QTreeWidgetItem([filename])
                        child.setIcon(0,self.docIcon)
                        item.addChild(child)
                        path=os.path.join(dir,filename)
                        child.setData(0,FileRole,path)
                        self.fileItems[path]=child
        
    def update(self):
        self.main=None
        self.src=None
        self.clear()
        self.folderIcon=utils.loadIcon('folder')
        self.docIcon=utils.loadIcon('doc')

        if not os.path.exists(self.root):
            return
        self.rootItem=QtGui.QTreeWidgetItem([self.root])
        self.rootItem.setIcon(0,self.folderIcon)
        self.rootItem.setData(0,DirectoryRole,self.root)
        self.addTopLevelItem(self.rootItem)
        
        self.fileItems={}
        self.scanDirectory('src')
        self.scanDirectory('include')
        self.loadSettings()
        if self.sorting:
            self.sortItems(0,QtCore.Qt.AscendingOrder)
    
    def setWorkspacePath(self,path):
        self.saveBreakpoints()
        self.root=path
        self.wsini=os.path.join(self.root,'settings.ini')
        s=QtCore.QSettings()
        s.setValue('workspace',path)
        s.sync()
        self.update()
        self.loadBreakpoints()
        
    def loadBreakpoints(self):
        settings=self.settings()
        allbps=settings.value('breakpoints','').toString()
        self.mainWindow.breakpoints.load(allbps)

    def saveBreakpoints(self):
        settings=self.settings()
        allbps=self.mainWindow.breakpoints.save()
        settings.setValue('breakpoints',allbps)
        
    def addProjectsToTree(self,root):
        def addSubItems(src,dst):
            for i in xrange(0,src.childCount()):
                item=src.child(i)
                ditem=QtGui.QTreeWidgetItem([item.text(0)])
                ditem.setData(0,DirectoryRole,item.data(0,DirectoryRole))
                dst.addChild(ditem)
                addSubItems(item,ditem)
        root.setData(0,DirectoryRole,self.root)
        if self.src:
            addSubItems(self.src,root)

    def saveTabs(self,tabs):
        ws=self.settings()
        if (tabs.count()>0):
            cur=tabs.currentIndex()
            path=tabs.tabToolTip(cur)
            ws.setValue('curtab',path)
            n=tabs.count()
            opentabs=[]
            for i in xrange(0,n):
                path=tabs.tabToolTip(i)
                opentabs.append(path)
            ws.setValue('opentabs',','.join(opentabs))
        else:
            ws.setValue('curtab','')
            ws.setValue('opentabs','')
        ws.sync()

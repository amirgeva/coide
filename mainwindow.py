from PyQt4 import QtCore
from PyQt4 import QtGui
import os

from qutepart import Qutepart
from workspace import WorkSpace
import output
from consts import *
from gdbwrapper import *
#import parseutils
from watchestree import WatchesTree
import utils
import genmake
import stat
from subprocess import call

class MainWindow(QtGui.QMainWindow):
    """ Main IDE Window

    Contains the main code view, along with docking panes for: source files,    
    watches, call stack, and output
    
    """
    
    def __init__(self,rootDir,parent=None):
        """ Initialize.  rootDir indicates where data files are located """
        super(MainWindow,self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(1024,768))

        self.currentLine=0
        self.currentFile=''
        self.rootDir=rootDir
        utils.setIconsDir(os.path.join(rootDir,"icons"))
        
        self.setWindowIcon(QtGui.QIcon(os.path.join(rootDir,'icons','bug.png')))

        self.generateQueue=set()        
        self.editors={}
        self.central=QtGui.QTabWidget()
        self.setCentralWidget(self.central)
        
        self.setupMenu()
        self.setupToolbar(rootDir)
        self.showWorkspacePane()
        self.showOutputPane()

        s=QtCore.QSettings()
        self.config=s.value("config").toString()
        if self.config=='':
            self.config="Debug"
        self.configCombo.setCurrentIndex(0 if self.config=='Debug' else 1)
        self.workspaceTree.setConfig(self.config)
        
        self.setAllFonts()
        
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.debugger=None
        self.runningWidget=None
        
        self.generateTimer=QtCore.QTimer()
        self.generateTimer.timeout.connect(self.autoGenerate)
        self.generateTimer.start(1000)

    def closeEvent(self, event):
        """ Called before the application window closes

        Informs sub-windows to prepare and saves window settings
        to allow future sessions to look the same
        
        """
        #self.editor.closingApp()
        self.timer.stop()
        if self.debugger:
            self.debugger.closingApp()
        while self.central.count()>0:
            self.closeFile()
        settings = QtCore.QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.sync()
        super(MainWindow,self).closeEvent(event)

    def setupMenu(self):
        """ Creates the application main menu 
        
        The action handlers are also mapped from the toolbar icons
        
        """
        bar=self.menuBar()
        m=bar.addMenu('&File')
        m.addAction(QtGui.QAction('Open &Workspace',self,triggered=self.openWorkspace))
        m.addAction(QtGui.QAction('&Save',self,shortcut='Ctrl+S',triggered=self.saveFile))
        m.addAction(QtGui.QAction('Save &As',self,triggered=self.saveAsFile))
        m.addAction(QtGui.QAction('&Close File',self,shortcut='Ctrl+F4',triggered=self.closeFile))
        
        m=bar.addMenu('&Build')
        m.addAction(QtGui.QAction('&Build',self,shortcut='F7',triggered=self.build))
        m.addAction(QtGui.QAction('&Clean',self,triggered=self.clean))
        m.addAction(QtGui.QAction('&Rebuild',self,shortcut='Shift+F7',triggered=self.rebuild))
        
        m=bar.addMenu('&Debug')
        m.addAction(QtGui.QAction('&Run',self,shortcut='Ctrl+F5',triggered=self.runProject))
        m.addAction(QtGui.QAction('&Start/Continue Debugger',self,shortcut='F5',triggered=self.startDebug))
        ma=m.addMenu('Actions')
        ma.addAction(QtGui.QAction('&Step',self,shortcut='F11',triggered=self.actStep))
        ma.addAction(QtGui.QAction('&Next',self,shortcut='F10',triggered=self.actNext))
        ma.addAction(QtGui.QAction('Step &Out',self,shortcut='Shift+F11',triggered=self.actOut))
        ma.addAction(QtGui.QAction('&Break',self,shortcut='Ctrl+C',triggered=self.actBreak))
        ma.addAction(QtGui.QAction('Sto&p',self,shortcut='Shift+F5',triggered=self.actStop))
        ma=m.addMenu('&Breakpoints')
        ma.addAction(QtGui.QAction('&Clear',self,triggered=self.clearBreakpoints))
        
        #m=bar.addMenu('&Debug')
        #m.addAction(QtGui.QAction('&Step',self,shortcut='F11',triggered=self.actStep))
        #m.addAction(QtGui.QAction('&Next',self,shortcut='F10',triggered=self.actNext))
        #m.addAction(QtGui.QAction('Step &Out',self,shortcut='Shift+F11',triggered=self.actOut))
        #m.addAction(QtGui.QAction('&Continue',self,shortcut='F5',triggered=self.actCont))
        #m.addAction(QtGui.QAction('&Break',self,shortcut='Ctrl+C',triggered=self.actBreak))
        #m.addAction(QtGui.QAction('Sto&p',self,shortcut='Shift+F5',triggered=self.actStop))
        #m=bar.addMenu('&Breakpoints')
        #m.addAction(QtGui.QAction('&Clear',self,triggered=self.clearBreakpoints))
        m=bar.addMenu('&Settings')
        m.addAction(QtGui.QAction('&Fonts',self,triggered=self.settingsFonts))

    def setupToolbar(self,rootDir):
        """ Creates the application main toolbar """
        tb=self.addToolBar('Actions')
        tb.setObjectName("Toolbar")
        dir=os.path.join(rootDir,'icons')
        tb.addAction(utils.loadIcon('gear'),'Generate Makefiles').triggered.connect(self.generateA)
        self.configCombo=self.createConfigCombo(tb)
        tb.addWidget(self.configCombo)
        tb.addAction(utils.loadIcon('step.png'),'Step').triggered.connect(self.actStep)
        tb.addAction(utils.loadIcon('next.png'),'Next').triggered.connect(self.actNext)
        tb.addAction(utils.loadIcon('out.png'),'Out').triggered.connect(self.actOut)
        tb.addAction(utils.loadIcon('cont.png'),'Continue').triggered.connect(self.actCont)
        tb.addAction(utils.loadIcon('break.png'),'Break').triggered.connect(self.actBreak)
        tb.addAction(utils.loadIcon('stop.png'),'Stop').triggered.connect(self.actStop)
        #self.addToolBar(tb)

    def settingsFonts(self):
        """ Edit the font settings for the code window and various panes """
        from settings import FontSettingsDialog
        d=FontSettingsDialog()
        if d.exec_():
            self.setAllFonts()
            
    def loadFont(self,name,target):
        """ Load previously saved font settings """
        settings=QtCore.QSettings()
        fb=settings.value(name).toByteArray()
        if not fb is None:
            buf=QtCore.QBuffer(fb)
            buf.open(QtCore.QIODevice.ReadOnly)
            font=QtGui.QFont()
            QtCore.QDataStream(fb) >> font
            target.setFont(font)
        else:
            target.setFont(QtGui.QFont('Monospace',14))
        
    def setAllFonts(self):
        """ Apply fonts to the various sub-windows """
        for e in self.editors:
            self.loadFont('codefont',self.editors.get(e))
        #self.loadFont('watchesfont',self.watchesTree)
        #self.loadFont('watchesfont',self.stackList)
        self.loadFont('watchesfont',self.outputEdit)
        self.loadFont('sourcesfont',self.workspaceTree)
        
    def buildSpecific(self,path):
        self.saveAll()
        self.autoGenerate()
        if len(path)>0:
            utils.execute(self.outputEdit,path,'/usr/bin/make',self.config)
        
    def build(self):
        self.buildSpecific(self.workspaceTree.mainPath())
            
    def clean(self):
        path=self.workspaceTree.mainPath()
        if len(path)>0:
            utils.execute(self.outputEdit,path,'/usr/bin/make','clean_{}'.format(self.config))
    
    def rebuild(self):
        self.clean()
        self.build()
        
    def autoGenerate(self):
        for path in self.generateQueue:
            print "Generating makefile for '{}'".format(path)
            genmake.generateDirectory(self.workspaceTree.root,path)
        self.generateQueue.clear()
        
    def generate(self):
        mb=QtGui.QMessageBox()
        mb.setText("Generate make files")
        mb.setInformativeText("Overwrite all make files?")
        mb.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        mb.setDefaultButton(QtGui.QMessageBox.Yes)
        rc=mb.exec_()
        if rc==QtGui.QMessageBox.Yes:
            genmake.generateTree(self.workspaceTree.root)
            utils.message("Done")

    def openWorkspace(self):
        d=QtGui.QFileDialog()
        d.setFileMode(QtGui.QFileDialog.Directory)
        d.setOption(QtGui.QFileDialog.ShowDirsOnly)
        if d.exec_():
            ws=(d.selectedFiles())[0]
            self.workspaceTree.setWorkspacePath(ws)

    def saveTabFile(self,index):
        n=self.central.tabBar().count()
        if index>=0 and index<n:
            path=self.central.tabToolTip(index)
            editor=self.editors.get(path)
            if editor:
                doc=editor.document()
                if doc.isModified():
                    f=open(path,'w')
                    if not f:
                        utils.errorMessage('Cannot write file: {}'.format(path))
                        return
                    f.write(doc.toPlainText())
                    f.close()
                    doc.setModified(False)
                    dir=os.path.dirname(path)
                    print "Adding '{}' to generate queue".format(dir)
                    self.generateQueue.add(dir)
            

    def saveFile(self):
        n=self.central.tabBar().count()
        if n>0:
            self.saveTabFile(self.central.currentIndex())
                    
    def saveAll(self):
        n=self.central.tabBar().count()
        for i in xrange(0,n):
            self.saveTabFile(i)

    def saveAsFile(self):
        pass

    def closeFile(self):
        n=self.central.tabBar().count()
        if n>0:
            index=self.central.currentIndex()
            path=self.central.tabToolTip(index)
            editor=self.editors.get(path)
            if editor:
                doc=editor.document()
                if doc.isModified():
                    mb = QtGui.QMessageBox()
                    mb.setText("{} has been modified.".format(os.path.basename(path)))
                    mb.setInformativeText("Do you want to save your changes?")
                    mb.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
                    mb.setDefaultButton(QtGui.QMessageBox.Save)
                    rc = mb.exec_()
                    if rc == QtGui.QMessageBox.Save:
                        f=open(path,'w')
                        if not f:
                            utils.errorMessage('Cannot write file: {}'.format(path))
                            return
                        f.write(doc.toPlainText())
                        f.close()
                    elif rc == QtGui.QMessageBox.Cancel:
                        return
                del self.editors[path]
                self.central.removeTab(index)
            

    def showWorkspacePane(self):
        """ Creates a docking pane that shows a list of source files """
        self.paneWorkspace=QtGui.QDockWidget("Workspace",self)
        self.paneWorkspace.setObjectName("Workspace")
        self.paneWorkspace.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.workspaceTree=WorkSpace(self.paneWorkspace,self)
        self.workspaceTree.depsChanged.connect(self.generate)
        #self.workspaceTree.itemClicked.connect(lambda item: self.loadItem(item))
        self.paneWorkspace.setWidget(self.workspaceTree)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.paneWorkspace)
        self.updateWorkspace()
        self.workspaceTree.doubleClicked.connect(self.docDoubleClicked)
        
    def updateWorkspace(self):
        self.workspaceTree.update()
        
    def setActiveSourceFile(self,path):
        if path in self.editors:
            editor=self.editors.get(path)
            n=self.central.tabBar().count()
            for i in xrange(0,n):
                if self.central.widget(i) == editor:
                    self.central.tabBar().setCurrentIndex(i)
                    return True
        return False
        
    def fixPath(self,path):
        if path.startswith(self.rootDir):
            path=os.path.relpath(path,self.rootDir)
        return path
        
    def openSourceFile(self,path):
        path=self.fixPath(path)
        if self.setActiveSourceFile(path):
            return True
        else:
            try:
                f=open(path,"r")
                if not f:
                    return False
                lines=f.readlines()
                if lines:
                    firstLine=lines[0]
    
                    editor=Qutepart()
                    editor.detectSyntax(sourceFilePath=path, firstLine=firstLine)
                    editor.lineLengthEdge = 1024
                    editor.drawIncorrectIndentation = True
                    editor.drawAnyWhitespace = False
                    editor.indentUseTabs = False
                    editor.text="".join(lines)
                    editor.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
                    index=self.central.addTab(editor,os.path.basename(path))
                    self.central.setTabToolTip(index,path)
                    self.editors[path]=editor
                    self.loadFont('codefont',editor)
                    self.central.tabBar().setCurrentIndex(index)
                    return True
            except IOError,e:
                return False
        return False

    def docDoubleClicked(self,index):
        item=self.workspaceTree.currentItem()
        path=item.data(0,FileRole).toString()
        if len(path)>0:
            self.openSourceFile(path)

    def goToSource(self,path,row,col,color=''):
        path=self.fixPath(path)
        if self.openSourceFile(path):
            editor=self.editors.get(path)
            if editor:
                self.setActiveSourceFile(path)
                c=editor.textCursor()
                c.movePosition(QtGui.QTextCursor.Start)
                c.movePosition(QtGui.QTextCursor.Down,n=row-1)
                c.movePosition(QtGui.QTextCursor.Right,n=col-1)
                editor.setTextCursor(c)
                editor.ensureCursorVisible()
                if len(color)>0:
                    editor.colorLine(row,color)
        
    def showCallStackPane(self):
        self.paneStack=QtGui.QDockWidget("Call Stack",self)
        self.paneStack.setObjectName("CallStack")
        self.paneStack.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.stackList=QtGui.QListWidget(self.paneStack)
        self.paneStack.setWidget(self.stackList)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.paneStack)
    
    def showWatchesPane(self):
        self.paneWatches=QtGui.QDockWidget("Watches",self)
        self.paneWatches.setObjectName("Watches")
        self.paneWatches.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.watchesTree=WatchesTree(self.paneWatches)
        self.watchesTree.setColumnCount(2)
        self.watchesTree.setHeaderLabels(['Name','Value'])
        self.paneWatches.setWidget(self.watchesTree)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.paneWatches)
        
        self.watchesTree.addTopLevelItem(QtGui.QTreeWidgetItem(['* Double-Click for new watch']))
        self.watchesTree.resizeColumnToContents(0)
        self.watchesTree.itemDoubleClicked.connect(lambda item,column : self.watchDoubleClicked(item,column))
        self.loadWatches()
        
        
    def showOutputPane(self):        
        self.paneOutput=QtGui.QDockWidget("Output",self)
        self.paneOutput.setObjectName("Output")
        self.paneOutput.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.outputEdit=output.OutputWidget(self.paneOutput,self)
        self.outputEdit.setReadOnly(True)
        self.paneOutput.setWidget(self.outputEdit)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.paneOutput)

    def watchDoubleClicked(self,item,column):
        """ Edits existing watches, or adds a new watch """
        changed=False
        index=self.watchesTree.indexOfTopLevelItem(item)
        if item.text(column)=='* Double-Click for new watch':
            res=QtGui.QInputDialog.getText(self,'New Watch','Expression')
            expr=res[0]
            if len(expr)>0 and res[1]:
                self.watchesTree.insertTopLevelItem(index,QtGui.QTreeWidgetItem([expr]))
                changed=True
                self.updateWatches()
        else:
            watch=item.text(0)
            res=QtGui.QInputDialog.getText(self,"Edit Watch",'Expression',text=watch)
            watch=res[0]
            if res[1]:
                changed=True
                if len(watch)>0:
                    item.setText(0,watch)
                    self.updateWatches()
                else:
                    self.watchesTree.takeTopLevelItem(index)
        if changed:
            self.saveWatches()


    def createConfigCombo(self,parent):
        configCombo=QtGui.QComboBox(parent)
        configCombo.addItem("Debug")
        configCombo.addItem("Release")
        configCombo.currentIndexChanged.connect(self.configChanged)
        return configCombo
        
    def configChanged(self,index):
        configs=['Debug','Release']
        self.config=configs[index]
        s=QtCore.QSettings()
        s.setValue("config",self.config)
        s.sync()
        self.workspaceTree.setConfig(self.config)
        #print "Config changed to: {}".format(configs[index])
        
    def addOutputText(self,added):
        """ Append the new text captured
        
        Text is appended to the end of existing text and the widget
        is scrolled to show the end 
        
        """
        text=self.outputEdit.toPlainText()
        self.outputEdit.setPlainText(text+added)
        c=self.outputEdit.textCursor()
        c.movePosition(QtGui.QTextCursor.End)
        self.outputEdit.setTextCursor(c)
        self.outputEdit.ensureCursorVisible()
        
    def runProject(self):
        path='/tmp/coide_run.sh'
        f=open(path,'w')
        dir=self.workspaceTree.getDebugDirectory()
        cmd=self.workspaceTree.getExecutablePath()
        params=self.workspaceTree.getDebugParams()
        if len(params)>0:
            cmd=cmd+" "+params
        f.write('#!/bin/sh\ncd {}\n{}\nread -r -p "Press any key..." key\n'.format(dir,cmd))
        f.close()
        os.chmod(path,stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR)
        call(['xterm','-fn','10x20','-e',path])
        os.remove(path)
        
    def getCurrentFile(self):
        if self.central.count()==0:
            return ''
        return self.central.tabToolTip(self.central.currentIndex())
        
    def getCurrentEditor(self):
        path=self.getCurrentFile()
        if len(path)>0:
            return self.editors.get(path)
        
    def updatePosition(self):
        """ Query current position and update the code view """
        (path,line)=self.debugger.getCurrentPos()
        changed=(self.currentLine!=line)
        if len(path)>0 and self.getCurrentFile()!=path:
            self.openSourceFile(path)
        e=self.editors.get(path)
        if e:
            e.colorLine(line,'#0080ff')
        #self.editor.code.setCurrentLine(self.currentFile,self.currentLine)
        
    def saveWatches(self):
        """ Save all watches to settings, for future sessions """
        res=[]
        n=self.watchesTree.topLevelItemCount()-1
        for i in xrange(0,n):
            item=self.watchesTree.topLevelItem(i)
            if len(res)>0:
                res.append(';')
            res.append(item.text(0))
        settings=QtCore.QSettings()
        key='watches:{}'.format(self.debugger.debugged)
        settings.setValue(key,''.join(res))
        
    def loadWatches(self):
        """ Load all previous session watches from settings """
        while self.watchesTree.topLevelItemCount()>1:
            self.watchesTree.takeTopLevelItem(0)
        settings=QtCore.QSettings()
        key='watches:{}'.format(self.debugger.debugged)
        val=settings.value(key,'').toString()
        if len(val)>0:
            arr=val.split(';')
            if len(arr)>0:
                res=[]
                for watch in arr:
                    res.append(QtGui.QTreeWidgetItem([watch]))
                self.watchesTree.insertTopLevelItems(0,res)
        
    def updateWatches(self):
        """ Re-evaluate the value of each watch and update view """
        n=self.watchesTree.topLevelItemCount()-1
        for i in xrange(0,n):
            item=self.watchesTree.topLevelItem(i)
            item.takeChildren()
            expr=item.text(0)
            res=self.debugger.evaluate(expr)
            if len(res)==0:
                item.setText(1,'')
            else:
                if res[0]=='string' or res[0]=='number':
                    item.setText(1,res[1])
                elif res[0]=='vector' or res[0]=='list':
                    del res[0]
                    parseutils.addSequence(item,res)
                elif res[0]=='map':
                    del res[0]
                    parseutils.addMapping(item,res)
                elif res[0]=='struct':
                    item.setText(1,parseutils.flatten(res))
                    del res[0]
                    parseutils.addMapping(item,res)
                    
    def updateCallstack(self):
        bt=self.debugger.getBackTrace()
        self.stackList.clear()
        for line in bt:
            self.stackList.addItem(line)
    
        
    def startDebug(self):
        if self.debugger:
            self.actCont()
            return
        cmd=[self.workspaceTree.getExecutablePath()]
        args=self.workspaceTree.getDebugParams().split()
        for a in args:
            cmd.append(a)
        self.debugger=GDBWrapper(cmd)
        self.showWatchesPane()
        self.showCallStackPane()
        self.timer.start(50)
        
    def stopDebugger(self):
        if self.debugger:
            self.debugger.quitDebugger()
            self.debugger=None        
            self.paneWatches.close()
            self.paneStack.close()
            self.timer.stop()
        
    def clearBreakpoints(self):
        if self.debugger:
            self.debugger.clearBreakpoints()

    def actStep(self):
        if self.debugger:
            self.debugger.actStep()

    def actNext(self):
        if self.debugger:
            self.debugger.actNext()

    def actOut(self):
        if self.debugger:
            self.debugger.actOut()

    def actCont(self):
        if self.debugger:
            e=self.getCurrentEditor()
            if e:
                e.colorLine(0,'')
            self.debugger.actCont()

    def actBreak(self):
        if self.debugger:
            self.debugger.actBreak()

    def actStop(self):
        if self.debugger:
            self.debugger.actStop()

    
    def update(self):
        """ Called every 50ms to check if a change in debugger state occurred
        
        Basically this is waiting for a change of state, indicated by:
        * self.debugger.changed
        
        If a change is detected, everything is re-evaluated and drawn
        
        """
        if self.debugger:
            text=self.debugger.update()
            if len(text)>0:
                self.addOutputText(text)
            if self.debugger.changed:
                self.updatePosition()
                self.updateWatches()
                self.updateCallstack()
                self.debugger.changed=False
            if not self.debugger.running:
                self.stopDebugger()
        # If the debugger is active running the program,
        # create an indication using an animation in the top left
        # corner of the application window
        if self.debugger and self.debugger.active:
            if self.runningWidget is None:
                from running import RunningWidget
                self.runningWidget=RunningWidget(self)
                self.runningWidget.show()
        elif not self.runningWidget is None:
            self.runningWidget.close()
            self.runningWidget=None

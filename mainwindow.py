from PyQt4 import QtCore
from PyQt4 import QtGui
import os
#from codeedit import CodeEditor
from qutepart import Qutepart
from workspace import WorkSpace
import output
from consts import *
#import parseutils
#from watchestree import WatchesTree
import utils
import genmake

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
        
        self.setWindowIcon(QtGui.QIcon(os.path.join(rootDir,'icons','bug.png')))
        
        self.editors={}
        self.central=QtGui.QTabWidget()
        self.setCentralWidget(self.central)
        
        self.setupMenu()
        self.setupToolbar(rootDir)
        self.showWorkspacePane()
        self.showOutputPane()

    def loadIcon(self,name):
        return QtGui.QIcon(os.path.join(self.rootDir,'icons',name+'.png'))

    def closeEvent(self, event):
        """ Called before the application window closes

        Informs sub-windows to prepare and saves window settings
        to allow future sessions to look the same
        
        """
        #self.editor.closingApp()
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
        m.addAction(QtGui.QAction('&Close File',self,shortcut='Ctrl+F4',triggered=self.closeFile))
        
        m=bar.addMenu('&Build')
        m.addAction(QtGui.QAction('&Build',self,shortcut='F7',triggered=self.build))
        m.addAction(QtGui.QAction('&Clean',self,triggered=self.clean))
        m.addAction(QtGui.QAction('&Rebuild',self,shortcut='Shift+F7',triggered=self.rebuild))
        
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
        tb.addAction(self.loadIcon('gear'),'Generate').triggered.connect(self.generate)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'step.png')),'Step').triggered.connect(self.actStep)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'next.png')),'Next').triggered.connect(self.actNext)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'out.png')),'Out').triggered.connect(self.actOut)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'cont.png')),'Continue').triggered.connect(self.actCont)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'break.png')),'Break').triggered.connect(self.actBreak)
        #tb.addAction(QtGui.QIcon(os.path.join(dir,'stop.png')),'Stop').triggered.connect(self.actStop)
        self.addToolBar(tb)

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
        self.loadFont('codefont',self.editor.code)
        self.loadFont('watchesfont',self.watchesTree)
        self.loadFont('watchesfont',self.stackList)
        self.loadFont('watchesfont',self.outputEdit)
        self.loadFont('sourcesfont',self.FilesViewList)
        
        
    def build(self):
        path=self.workspaceTree.mainPath()
        if len(path)>0:
            utils.execute(self.outputEdit,path,'/usr/bin/make')
            
    def clean(self):
        pass
    
    def rebuild(self):
        pass
        
    def generate(self):
        mb=QtGui.QMessageBox()
        mb.setText("Generate make files")
        mb.setInformativeText("Overwrite all make files?")
        mb.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        mb.setDefaultButton(QtGui.QMessageBox.Yes)
        rc=mb.exec_()
        if rc==QtGui.QMessageBox.Yes:
            genmake.generateTree(os.path.join(self.rootDir,"src"))
            utils.message("Done")

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
                    mb.setText("The document has been modified.")
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
        #self.workspaceTree.itemClicked.connect(lambda item: self.loadItem(item))
        self.paneWorkspace.setWidget(self.workspaceTree)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.paneWorkspace)
        self.updateWorkspace()
        self.workspaceTree.doubleClicked.connect(self.docDoubleClicked)
        
    def updateWorkspace(self):
        folderIcon=self.loadIcon('folder')
        docIcon=self.loadIcon('doc')
        self.workspaceTree.update(folderIcon,docIcon)
        
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
                self.central.tabBar().setCurrentIndex(index)
                return True
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
                print "Going to '{}':{}:{}".format(path,row,col)
                self.setActiveSourceFile(path)
                c=editor.textCursor()
                c.movePosition(QtGui.QTextCursor.Start)
                c.movePosition(QtGui.QTextCursor.Down,n=row-1)
                c.movePosition(QtGui.QTextCursor.Right,n=col-1)
                editor.setTextCursor(c)
                editor.ensureCursorVisible()
                if len(color)>0:
                    editor.colorLine(row,color)
        
    def showOutputPane(self):        
        self.paneOutput=QtGui.QDockWidget("Output",self)
        self.paneOutput.setObjectName("Output")
        self.paneOutput.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.outputEdit=output.OutputWidget(self.paneOutput,self)
        self.outputEdit.setReadOnly(True)
        self.paneOutput.setWidget(self.outputEdit)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,self.paneOutput)
        
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
        


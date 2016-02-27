from PyQt4 import QtCore,QtGui
import uis
import os
import imp
from buildsettings import check

class Plugin(QtCore.QObject):
    def __init__(self,dir,filename):
        super(Plugin,self).__init__()
        self.filename=filename
        self.dir=dir
        self.shortcut=QtCore.QSettings().value('plugin_'+filename).toString()
        self.action=None
    
    def activated(self):
        print "Triggered"

    def load(self):
        fp=None
        try:
            self.name=self.filename[0:-3]
            path=os.path.join(self.dir,self.filename)
            (fp, pathname, description)=imp.find_module(self.name,[self.dir])
            self.module=imp.load_module(self.name,fp,pathname,description)
            if 'activate' in dir(self.module):
                print "Found activate in {}".format(self.name)
                self.activate=getattr(self.module,'activate')
                if self.shortcut:
                    print "Creating action shortcut={}".format(self.shortcut)
                    self.action=QtGui.QAction(self,shortcut=self.shortcut,triggered=self.activated)
                return True
            return False
        except ImportError,e:
            print "Failed to import {}".format(filename)
            return False
        finally:
            if fp:
                fp.close()
            

class PluginsManager(QtCore.QObject):
    def __init__(self):
        super(PluginsManager,self).__init__()
        s=QtCore.QSettings()
        self.plugins={}
        self.dir=s.value('pluginsDir').toString()
        self.loadPlugins()
        
    def loadPlugins(self):
        if self.dir:
            files=os.listdir(self.dir)
            files=[f for f in files if f.endswith('.py')]
            for f in files:
                p=Plugin(self.dir,f)
                if p.load():
                    self.plugins[p.name]=p
                
class ShortcutDialog(QtGui.QDialog):
    def __init__(self,shortcut,parent=None):
        super(ShortcutDialog,self).__init__(parent)
        uis.loadDialog('shortcut',self)
        keys=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        keys.extend('F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12'.split(','))
        for k in keys:
            self.keyCB.addItem(k)
        self.shortcut=shortcut
        s=shortcut.split('+')
        for p in s:
            if p=='Ctrl':
                check(self.ctrlCB,True)
            if p=='Alt':
                check(self.altCB,True)
            if p=='Meta':
                check(self.metaCB,True)
            if p=='Shift':
                check(self.shiftCB,True)
        index=self.keyCB.findText(s[-1])
        self.keyCB.setCurrentIndex(index)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        
    def accept(self):
        from buildsettings import getCheck
        s=[]
        if getCheck(self.ctrlCB):
            s.append('Ctrl+')
        if getCheck(self.altCB):
            s.append('Alt+')
        if getCheck(self.metaCB):
            s.append('Meta+')
        if getCheck(self.shiftCB):
            s.append('Shift+')
        s.append(self.keyCB.currentText())
        self.shortcut=''.join(s)
        super(ShortcutDialog,self).accept()

class PluginsDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(PluginsDialog,self).__init__(parent)
        uis.loadDialog('plugins',self)
        s=QtCore.QSettings()
        self.dir=s.value('pluginsDir','').toString()
        self.pluginsDirectory.setText(self.dir)
        self.dirBrowse.clicked.connect(self.browsePluginsDir)
        self.pluginsTable.setColumnCount(2);
        self.pluginsTable.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem('Plugin'))
        self.pluginsTable.setHorizontalHeaderItem(1,QtGui.QTableWidgetItem('Shortcut'))
        self.updatePlugins()
        self.pluginsTable.resizeRowsToContents()

    def updatePlugins(self):
        if self.dir:
            s=QtCore.QSettings()
            files=os.listdir(self.dir)
            files=[f for f in files if f.endswith('.py')]
            self.pluginsTable.setRowCount(len(files))
            for i in xrange(0,len(files)):
                name=os.path.basename(files[i])
                item=QtGui.QTableWidgetItem(name)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.pluginsTable.setItem(i,0,item)
                shortcut=s.value('plugin_'+name).toString()
                self.pluginsTable.setItem(i,1,QtGui.QTableWidgetItem(shortcut))
                
    def contextMenuEvent(self,event):
        menu=QtGui.QMenu()
        menu.addAction(QtGui.QAction('Select Keys',self,triggered=self.shortcutDialog))
        menu.exec_(event.globalPos())
        
    def shortcutDialog(self):
        row=self.pluginsTable.currentRow()
        item=self.pluginsTable.currentItem()
        d=ShortcutDialog(item.text())
        if d.exec_():
            scriptName=self.pluginsTable.item(row,0).text()
            item.setText(d.shortcut)
            QtCore.QSettings().setValue('plugin_'+scriptName,d.shortcut)
                
    def browsePluginsDir(self):
        d=QtGui.QFileDialog.getExistingDirectory(directory=self.dir)
        if d:
            self.dir=d
            self.pluginsDirectory.setText(d)
            self.updatePlugins()
        
    def save(self):
        s=QtCore.QSettings()
        s.setValue('pluginsDir',self.dir)


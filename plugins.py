from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets
import uis
import os
import importlib
import importlib.util
import globals
from buildsettings import check

class Plugin(QtCore.QObject):
    def __init__(self,dir,filename):
        super(Plugin,self).__init__()
        self.filename=filename
        self.dir=dir
        self.shortcut=QtCore.QSettings().value('plugin_'+filename)
        self.action=None
    
    def activated(self):
        c=globals.mw.createPluginCuror()
        if c:
            self.activate(c)

    def load(self):
        try:
            self.name=self.filename[0:-3]
            path=os.path.join(self.dir,self.filename)
            spec=importlib.util.spec_from_file_location(self.name, path)
            self.module=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.module)
            if 'activate' in dir(self.module):
                self.activate=getattr(self.module,'activate')
                if self.shortcut:
                    self.action=QtGui.QAction(self.name,self,shortcut=self.shortcut,triggered=self.activated)
                return True
            return False
        except ImportError as e:
            print("Failed to import {}".format(self.filename))
            return False
            

class PluginsManager(QtCore.QObject):
    def __init__(self):
        super(PluginsManager,self).__init__()
        s=QtCore.QSettings()
        self.plugins={}
        self.dir=s.value('pluginsDir')
        self.loadPlugins()
        
    def loadPlugins(self):
        if self.dir:
            files=os.listdir(self.dir)
            files=[f for f in files if f.endswith('.py')]
            for f in files:
                p=Plugin(self.dir,f)
                if p.load():
                    self.plugins[p.name]=p
                    
    def addToMenu(self,menu):
        for name in self.plugins:
            menu.addAction(self.plugins.get(name).action)
                
class ShortcutDialog(QtWidgets.QDialog):
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

class PluginsDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(PluginsDialog,self).__init__(parent)
        uis.loadDialog('plugins',self)
        s=QtCore.QSettings()
        self.dir=s.value('pluginsDir','')
        self.pluginsDirectory.setText(self.dir)
        self.dirBrowse.clicked.connect(self.browsePluginsDir)
        self.pluginsTable.setColumnCount(2);
        self.pluginsTable.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem('Plugin'))
        self.pluginsTable.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem('Shortcut'))
        self.updatePlugins()
        self.pluginsTable.resizeRowsToContents()

    def updatePlugins(self):
        if self.dir:
            s=QtCore.QSettings()
            files=os.listdir(self.dir)
            files=[f for f in files if f.endswith('.py')]
            self.pluginsTable.setRowCount(len(files))
            for i in range(0,len(files)):
                name=os.path.basename(files[i])
                item=QtWidgets.QTableWidgetItem(name)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.pluginsTable.setItem(i,0,item)
                shortcut=s.value('plugin_'+name)
                self.pluginsTable.setItem(i,1,QtWidgets.QTableWidgetItem(shortcut))
                
    def contextMenuEvent(self,event):
        menu=QtWidgets.QMenu()
        menu.addAction(QtGui.QAction('Select Keys',self,triggered=self.shortcutDialog))
        menu.exec(event.globalPosition().toPoint())
        
    def shortcutDialog(self):
        row=self.pluginsTable.currentRow()
        item=self.pluginsTable.currentItem()
        d=ShortcutDialog(item.text())
        if d.exec():
            scriptName=self.pluginsTable.item(row,0).text()
            item.setText(d.shortcut)
            QtCore.QSettings().setValue('plugin_'+scriptName,d.shortcut)
                
    def browsePluginsDir(self):
        d=QtWidgets.QFileDialog.getExistingDirectory(directory=self.dir)
        if d:
            self.dir=d
            self.pluginsDirectory.setText(d)
            self.updatePlugins()
        
    def save(self):
        s=QtCore.QSettings()
        s.setValue('pluginsDir',self.dir)


from PyQt4 import QtCore
from PyQt4 import QtGui
import uis
import os
import utils

class FontSettingsDialog(QtGui.QDialog):
    """
    Dialog for selection of fonts for the various windows and panes
    Currently 3 window groups are supported:
      * Code in the text editor
      * Tool windows, such as watches and call stack
      * Workspace tree
    """
    def __init__(self,parent=None):
        super(FontSettingsDialog,self).__init__(parent)
        self.fontsDict={}
        self.mainLayout=QtGui.QVBoxLayout()
        self.edFontButton,self.edFontText=self.addFontLayout("Code View Font","codefont")
        self.wtFontButton,self.wtFontText=self.addFontLayout("Watches Pane Font","watchesfont")
        self.flFontButton,self.flFontText=self.addFontLayout("Sources List Pane Font","sourcesfont")
        buttons=QtGui.QHBoxLayout()
        self.okButton=QtGui.QPushButton("Ok")
        buttons.addWidget(self.okButton)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton=QtGui.QPushButton("Cancel")
        buttons.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.reject)
        self.mainLayout.addLayout(buttons)
        self.setLayout(self.mainLayout)
        
    def addFontLayout(self,label,name):
        fontLayout=QtGui.QHBoxLayout()
        fontButton=QtGui.QPushButton("Select")
        fontText=QtGui.QTextEdit()
        fontButton.clicked.connect(lambda : self.selectFont(fontText))
        fontText.setText(label)
        fontText.setMaximumHeight(48)
        fontLayout.addWidget(fontButton)
        fontLayout.addWidget(fontText)
        self.fontsDict[name]=fontText
        self.mainLayout.addLayout(fontLayout)
        settings=QtCore.QSettings()
        if settings.contains(name):
            fb=settings.value(name).toByteArray()
            font=QtGui.QFont()
            QtCore.QDataStream(fb) >> font
            fontText.setFont(font)
        else:
            font=QtGui.QFont("Monospace",14)
            fontText.setFont(font)
        return fontButton,fontText
        
    def selectFont(self,textField):
        (font,ok)=QtGui.QFontDialog.getFont(textField.font())
        if ok:
            textField.setFont(font)
            
    def accept(self):
        settings=QtCore.QSettings()
        for name in self.fontsDict.keys():
            font=self.fontsDict.get(name).font()
            arr=QtCore.QByteArray()
            buf=QtCore.QBuffer(arr)
            buf.open(QtCore.QIODevice.WriteOnly)
            QtCore.QDataStream(buf) << font
            settings.setValue(name,arr)
        settings.sync()
        super(FontSettingsDialog,self).accept()

class GeneralSettingsDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(GeneralSettingsDialog,self).__init__(parent)
        uis.loadDialog('general_settings',self)
        s=QtCore.QSettings()
        self.sortFilesCB.setCheckState(QtCore.Qt.Checked if s.value('sortFiles',True).toBool() else QtCore.Qt.Unchecked)
        self.customPrinters.setCheckState(QtCore.Qt.Checked if s.value('customPrinters',True).toBool() else QtCore.Qt.Unchecked)
        self.clearCacheButton.clicked.connect(self.clearCache)
    
    def save(self):
        s=QtCore.QSettings()
        s.setValue('sortFiles',(self.sortFilesCB.checkState() == QtCore.Qt.Checked))
        s.setValue('customPrinters',(self.customPrinters.checkState() == QtCore.Qt.Checked))
        s.sync()
        
    def clearCache(self):
        s=QtCore.QSettings()
        s.remove('all_packages')
        s.sync()
        QtGui.QMessageBox.information(self,"Clear Cache","Restart IDE to reload...")
    

class EditorSettingsDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(EditorSettingsDialog,self).__init__(parent)
        uis.loadDialog('editor_settings',self)
        s=QtCore.QSettings()
        self.indentSpaces.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d+')))
        self.indentSpaces.setText(s.value('indent','2').toString())
        self.clangCB.setCheckState(QtCore.Qt.Checked if s.value('clangCompletion',True).toBool() else QtCore.Qt.Unchecked)

    def save(self):
        s=QtCore.QSettings()
        indent=2
        try:
            indent=int(self.indentSpaces.text())
        except ValueError:
            pass
        s.setValue('indent',indent)
        s.setValue('clangCompletion',(self.clangCB.checkState() == QtCore.Qt.Checked))
        s.sync()
     
class MacrosHelpDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(MacrosHelpDialog,self).__init__(parent)
        uis.loadDialog('macros_help',self)
        helpData={
            '${SELECTION}':'Substitute for the text selected in the editor when the template is activated',
            '${FILEPATH}':'Substitute for the full path of the current editor file',
            '${FILEBASE}':'Substitute for the current editor file name without an extension'
        }
        self.macrosTable.setRowCount(len(helpData))
        self.macrosTable.setColumnCount(2)
        row=0
        for m in helpData:
            self.macrosTable.setItem(row,0,QtGui.QTableWidgetItem(m))
            self.macrosTable.setItem(row,1,QtGui.QTableWidgetItem(helpData.get(m)))
            row=row+1
        self.macrosTable.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem('Macro'))
        self.macrosTable.setHorizontalHeaderItem(1,QtGui.QTableWidgetItem('Description'))
        self.macrosTable.resizeRowsToContents()
        
class TemplatesDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(TemplatesDialog,self).__init__(parent)
        uis.loadDialog('templates',self)
        s=QtCore.QSettings()
        self.dir=s.value('tmplDir','').toString()
        self.tmplDir.setText(self.dir)
        self.updateTemplates()
        self.templatesList.itemSelectionChanged.connect(self.selChanged)
        self.curEdit=''
        self.codeEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.addButton.clicked.connect(self.addClicked)
        self.delButton.clicked.connect(self.delClicked)
        self.macrosButton.clicked.connect(self.macrosClicked)
        self.tmplDirBrowseButton.clicked.connect(self.browseTmplDir)
        
    def updateTemplates(self):        
        self.templatesList.clear()
        templates=[]
        if self.dir:
            templates=os.listdir(self.dir)
            templates=[os.path.splitext(t)[0] for t in templates if t.endswith('.template')]
        if len(templates)>0:
            self.templatesList.addItems(templates)
        self.codeEdit.setPlainText('')
        
    def macrosClicked(self):
        MacrosHelpDialog().exec_()
    
    def browseTmplDir(self):
        d=QtGui.QFileDialog.getExistingDirectory(directory=self.dir)
        if d:
            self.dir=d
            self.tmplDir.setText(d)
            QtCore.QSettings().setValue('tmplDir',d)
            self.updateTemplates()

    def addClicked(self):
        if not self.dir:
            utils.errorMessage('Please set template directory first')
        else:
            (label,ok)=QtGui.QInputDialog.getText(self,"New Template","Template Name")
            if ok:
                self.templatesList.addItem(label)
                try:
                    f=open(os.path.join(self.dir,label+".template"),'w')
                    f.write("\n")
                    f.close()
                except IOError:
                    utils.errorMessage('Could not write template file at: {}'.format(self.dir))
                
        
    def delClicked(self):
        if self.curEdit:
            item=(self.templatesList.selectedItems())[0]
            self.templatesList.removeItemWidget(item)
            self.curEdit=''

    def saveCurrent(self):
        if self.curEdit:
            oldpath=os.path.join(self.dir,self.curEdit+".template")
            try:
                f=open(oldpath,'w')
                f.write(self.codeEdit.toPlainText())
                f.close()
            except IOError:
                utils.errorMessage('Cannot write file: {}'.format(oldpath))

    def selChanged(self):
        self.saveCurrent()
        sel=self.templatesList.selectedItems()
        if len(sel)==1:
            item=sel[0]
            label=item.text()
            path=os.path.join(self.dir,label+".template")
            try:
                f=open(path,'r')
                code=f.read()
                self.codeEdit.setPlainText(code)
                self.curEdit=label
            except IOError:
                utils.errorMessage('Cannot read file: {}'.format(path))
        
    def accept(self):
        self.saveCurrent()
        super(TemplatesDialog,self).accept()
        
    def save(self):
        pass
    

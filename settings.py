from PyQt4 import QtCore
from PyQt4 import QtGui
import uis

class FontSettingsDialog(QtGui.QDialog):
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


class EditorSettingsDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(EditorSettingsDialog,self).__init__(parent)
        uis.loadDialog('editor_settings',self)
        s=QtCore.QSettings()
        self.indentSpaces.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d+')))
        self.indentSpaces.setText(s.value('indent','2').toString())
        
    def save(self):
        s=QtCore.QSettings()
        indent=2
        try:
            indent=int(self.indentSpaces.text())
        except ValueError:
            pass
        s.setValue('indent',indent)
        s.sync()
        
        
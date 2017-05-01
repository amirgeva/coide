from PyQt4 import QtCore
from PyQt4 import QtGui
import uis

def check(cb,state):
    if state:
        cb.setCheckState(QtCore.Qt.Checked)
    else:
        cb.setCheckState(QtCore.Qt.Unchecked)

def getCheck(cb):
    return (cb.checkState() == QtCore.Qt.Checked)

class FindDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(FindDialog,self).__init__(parent)
        uis.loadDialog('find_replace',self)
        self.findButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.replaceButton.clicked.connect(self.replace)
        s=QtCore.QSettings()
        check(self.caseCB,s.value('find_case',False).toBool())
        check(self.backCB,s.value('find_back',False).toBool())
        check(self.wordsCB,s.value('find_words',False).toBool())
        check(self.allCB,s.value('find_all',False).toBool())
        self.findEdit.setText(s.value('find_text','').toString())
        self.replaceEdit.setText(s.value('find_replace_text','').toString())
        self.findEdit.setFocus(QtCore.Qt.OtherFocusReason)
        self.replaceClicked=False
        
    def setFindText(self,text):
        self.findEdit.setText(text)
        
    def accept(self):
        self.details={
            'find_case':getCheck(self.caseCB),
            'find_words':getCheck(self.wordsCB),
            'find_back':getCheck(self.backCB),
            'find_all':getCheck(self.allCB),
            'find_text':self.findEdit.text(),
            'find_replace_text':self.replaceEdit.text(),
        }
        s=QtCore.QSettings()
        for key in self.details:
            s.setValue(key,self.details.get(key))
        s.sync()
        self.details['find_replace']=self.replaceClicked
        super(FindDialog,self).accept()
        
    def replace(self):
        self.replaceClicked=True
        self.accept()
        
from PyQt4 import QtGui
import uis

class DependenciesDialog(QtGui.QDialog):
    def __init__(self,libs,parent=None):
        super(DependenciesDialog,self).__init__(parent)
        uis.loadDialog('deps',self)
        buttonNames=['ok','cancel','add','remove','up','down']
        for name in buttonNames:
            button=getattr(self,name+'Button')
            handler=getattr(self,name+'Pressed')
            button.clicked.connect(handler)
        self.libs=[]
        self.depsList.clear()
        for lib in libs:
            if len(lib.strip())>0:
                self.depsList.addItem(QtGui.QListWidgetItem(lib))

    def addButton(self,layout,text,callback):
        b=QtGui.QPushButton(text)
        b.clicked.connect(callback)
        layout.addWidget(b)

    def upPressed(self):
        cur=self.depsList.currentRow()
        if cur>0:
            item=self.depsList.takeItem(cur)
            self.depsList.insertItem(cur-1,item)
            self.depsList.setCurrentRow(cur-1)

    def downPressed(self):
        cur=self.depsList.currentRow()
        if cur<(self.depsList.count()-1):
            item=self.depsList.takeItem(cur)
            self.depsList.insertItem(cur+1,item)
            self.depsList.setCurrentRow(cur+1)

    def addPressed(self):
        res=QtGui.QInputDialog.getText(self,"Library Name","Library")
        if res[1]:
            lib=res[0]
            self.depsList.addItem(lib)
    
    def removePressed(self):
        i=self.depsList.currentRow()
        n=self.depsList.count()
        if i>=0 and i<n:
            self.depsList.takeItem(i)

    def cancelPressed(self):
        self.reject()
        
    def okPressed(self):
        n=self.depsList.count()
        self.libs=[]
        for i in xrange(0,n):
            lib=self.depsList.item(i).text()
            self.libs.append(lib)
        self.accept()
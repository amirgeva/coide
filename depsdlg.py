from PyQt4 import QtGui


class DependenciesDialog(QtGui.QDialog):
    def __init__(self,libs,parent=None):
        super(DependenciesDialog,self).__init__(parent)
        layout=QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.depsList=QtGui.QListWidget(self)
        layout.addWidget(self.depsList)
        buttonLayout=QtGui.QHBoxLayout()
        layout.addLayout(buttonLayout)
        self.addButton(buttonLayout,"Ok",self.okPressed)
        self.addButton(buttonLayout,"Cancel",self.cancelPressed)
        self.addButton(buttonLayout,"Add",self.addPressed)
        self.addButton(buttonLayout,"Remove",self.removePressed)
        self.libs=[]
        self.depsList.clear()
        for lib in libs:
            if len(lib.strip())>0:
                self.depsList.addItem(QtGui.QListWidgetItem(lib))

    def addButton(self,layout,text,callback):
        b=QtGui.QPushButton(text)
        b.clicked.connect(callback)
        layout.addWidget(b)

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
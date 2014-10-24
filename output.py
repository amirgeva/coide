import re
from PyQt4 import QtGui

posStrPattern=re.compile('(.+):(\d+):(\d+):')

class OutputWidget(QtGui.QPlainTextEdit):
    def __init__(self,pane,mainwin):
        super(OutputWidget,self).__init__(pane)
        self.mainWindow=mainwin
        self.input=[]
        
    def mouseDoubleClickEvent(self,event):
        c=self.textCursor()
        line=c.block().text()
        parts=line.split(' ')
        if len(parts)>0:
            posStr=parts[0]
            m=re.match(posStrPattern,posStr)
            if m:
                g=m.groups()
                path=g[0]
                row=int(g[1])
                col=int(g[2])
                self.mainWindow.goToSource(path,row,col,'#ff8080')

    def keyPressEvent(self,event):
        #print "{} : '{}'".format(event.key(),event.text())
        s=event.text()
        if len(s)>0:
            if s=='\r':
                s='\n'
            self.input.append(s)
        
    def getInput(self):
        res=self.input
        self.clearInput()
        return res
        
    def clearInput(self):
        self.input=[]
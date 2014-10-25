import re
from PyQt4 import QtGui, QtCore

posStrPattern=re.compile('(.+):(\d+):(\d+):')

class OutputWidget(QtGui.QPlainTextEdit):
    def __init__(self,pane,mainwin):
        super(OutputWidget,self).__init__(pane)
        self.mainWindow=mainwin
        self.input=[]
        self.blinking=False
        self.cursorVisible=False
        self.cursorTimer=QtCore.QTimer(self)
        self.cursorTimer.timeout.connect(self.updateCursor)
        
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
        
    def setBlinkingCursor(self,state):
        if state!=self.blinking:
            self.blinking=state
            if state:
                self.cursorTimer.start(500)
            else:
                self.cursorTimer.stop()
                if self.cursorVisible:
                    self.updateCursor()
                
    def paintEvent(self,event):
        super(OutputWidget,self).paintEvent(event)
        if self.cursorVisible:
            qp=QtGui.QPainter(self.viewport())
            r=self.cursorRect()
            r.setWidth(10)
            if self.hasFocus():
                qp.fillRect(r,QtCore.Qt.SolidPattern)
            else:
                qp.drawRect(r)
                
    def updateCursor(self):
        self.cursorVisible=not self.cursorVisible
        self.viewport().update()
        
        
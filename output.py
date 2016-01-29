import re
from PyQt4 import QtGui, QtCore

posStrPatterns=[
    re.compile('(.+):(\d+):(\d+):'),
    re.compile('\[(.+):(\d+)\]:')
]
tagPattern=re.compile('<[^<>]*>')

def removeTags(s):
    while True:
        m=re.search(tagPattern,s)
        if m:
            s=s[0:m.start()]+s[m.end():]
        else:
            break
    return s
    

class OutputWidget(QtGui.QPlainTextEdit):
    def __init__(self,pane,mainwin):
        super(OutputWidget,self).__init__(pane)
        self.mainWindow=mainwin
        self.input=[]
        self.blinking=False
        self.cursorVisible=False
        self.cursorTimer=QtCore.QTimer(self)
        self.cursorTimer.timeout.connect(self.updateCursor)
        self.errors=[]
        
    def mouseDoubleClickEvent(self,event):
        c=self.textCursor()
        line=c.block().text()
        parts=line.split(' ')
        if len(parts)>0:
            posStr=parts[0]
            for pat in posStrPatterns:
                m=re.match(pat,posStr)
                if m:
                    g=m.groups()
                    path=g[0]
                    row=int(g[1])
                    if len(g)>2:
                        col=int(g[2])
                    else:
                        col=1
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
        
    def highlightLine(self,row):
        c=self.textCursor()
        c.movePosition(QtGui.QTextCursor.Start,QtGui.QTextCursor.MoveAnchor)
        c.movePosition(QtGui.QTextCursor.NextBlock,QtGui.QTextCursor.MoveAnchor,row+1)
        c.movePosition(QtGui.QTextCursor.PreviousBlock,QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(c)
        self.ensureCursorVisible()        
        
    def appendLine(self,line):
        outputRow=self.blockCount()
        self.appendPlainText(line)
        p=line.find(' ')
        if p>0:
            posStr=line[0:p]
            rest=line[(p+1):]
            for pat in posStrPatterns:
                m=re.match(pat,posStr)
                if m:
                    g=m.groups()
                    path=g[0]
                    row=int(g[1])
                    if len(g)>2:
                        col=int(g[2])
                    else:
                        col=1
                    msg=removeTags(rest)
                    self.errors.append((path,row,col,msg,outputRow))
                
    def getNextError(self):
        if len(self.errors)==0:
            return None
        e=self.errors[0]
        del self.errors[0]
        self.errors.append(e)
        return e
        
    def clearAll(self):
        self.clear()
        self.errors=[]
        
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
        
        

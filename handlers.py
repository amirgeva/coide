from PyQt4 import QtGui
import re

class Handler(object):
    def __init__(self):
        self.lines=[]
        
    def addLine(self,line):
        self.lines.append(line)
        self.check()


class SignalHandler(Handler):
    def __init__(self):
        super(SignalHandler,self).__init__()
        self.sigpat='Program received signal ([A-Z]+), Aborted.'
        
    def check(self):
        l=self.lines[-1]
        m=re.search(self.sigpat,l)
        if m:
            g=m.groups()
            sig=g[0]
            QtGui.QMessageBox.critical(None,"Unhandled Signal",sig)
            
    
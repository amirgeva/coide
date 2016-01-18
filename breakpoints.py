from PyQt4 import QtCore, QtGui
import uis
import json

class Breakpoint(QtGui.QTextBlockUserData):
    def __init__(self,data=None):
        super(Breakpoint,self).__init__()
        self.block=None
        if data:
            self.data=data
        else:
            self.data={
                'enabled':True,
                'line':-1,
                'condition':''
            }
            
    def line(self):
        if self.block:
            return self.block.blockNumber()
        return self.data.get('line')
            
    def setBlock(self,block):
        self.block=block
        self.data['line']=block.blockNumber()
        block.setUserData(self)
        
    def isValid(self):
        if not self.block:
            return False
        return self.block.userData()==self
    
    def condition(self):
        return self.data.get('condition')
        
    def setCondition(self,s):
        self.data['condition']=s
        
    def isEnabled(self):
        return self.data.get('enabled')
        
    def able(self,state):
        if state:
            self.enable()
        else:
            self.disable()
    
    def enable(self):
        self.data['enabled']=True
        
    def disable(self):
        self.data['enabled']=False
        
    def save(self):
        return json.dumps(self.data)
        
    def load(self,s):
        self.data=json.loads(s)
        
class BreakpointList(list):
    def __init__(self,*args):
        list.__init__(self,*args)
        
    def removeInvalid(self):
        index=0
        res=False
        while index<len(self):
            if self[index].isValid():
                index=index+1
            else:
                del self[index]
                res=True
        return res
        
    def findIndex(self,blockNumber):
        i=0
        for bp in self:
            if bp.block:
                if bp.block.blockNumber()==blockNumber:
                    return i
            else:
                if bp.data.get('line')==blockNumber:
                    return i
            i=i+1
        return -1
        
    def find(self,blockNumber):
        index=self.findIndex(blockNumber)
        if index<0:
            return None
        return self[index]
        
    def __contains__(self,blockNumber):
        return self.findIndex(blockNumber)>=0


class BreakpointEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Breakpoint):
            return obj.data
        return json.JSONEncoder.default(self, obj)

class BreakpointsDB(QtCore.QObject):
    
    breakpointsChanged = QtCore.pyqtSignal()
    
#    def testPrint(self):
#        for path in self.breakpoints:
#            blist=self.breakpoints.get(path)
#            for bp in blist:
#                if bp.block:
#                    print '{}:{} - Valid={}'.format(path,bp.block.blockNumber(),bp.isValid())
    
    def __init__(self):
        super(BreakpointsDB,self).__init__()
        self.breakpoints={}
        
    def clear(self):
        self.breakpoints.clear()
        
    def printall(self):
        print self.breakpoints
        
    def paths(self):
        return self.breakpoints.keys()
        
    def updateLineNumbers(self,path):
        res=[]
        if path in self.breakpoints:
            bps=self.breakpoints.get(path)
            if bps.removeInvalid():
                res.append(path)
            for bp in bps:
                if bp.block:
                    bp.data['line']=bp.block.blockNumber()
        return res
        
    def pathBreakpoints(self,path):
        if not path in self.breakpoints:
            self.breakpoints[path]=BreakpointList()
        return self.breakpoints.get(path)
        
    def setBreakpoint(self,path,block):
        bps=self.pathBreakpoints(path)
        if not block.blockNumber() in bps:
            bp=Breakpoint()
            bp.setBlock(block)
            bps.append(bp)
            self.breakpointsChanged.emit()
        
#    def removeBreakpoint(self,path,line):
#        bps=self.pathBreakpoints(path)
#        del bps[line]
#        self.breakpointsChanged.emit()
        
    def getBreakpoint(self,path,line):
        return self.pathBreakpoints(path).find(line)
        
    def hasBreakpoint(self,path,line):
        if not path in self.breakpoints:
            return False
        bps=self.pathBreakpoints(path)
        return line in bps
        
    def toggleBreakpoint(self,editor):
        bps=self.pathBreakpoints(editor.path)
        block=editor.contextBlock
        index=bps.findIndex(block.blockNumber())
        if index>=0:
            del bps[index]
        else:
            b=Breakpoint()
            b.setBlock(block)
            bps.append(b)
        self.breakpointsChanged.emit()
        
    def update(self):
        self.breakpointsChanged.emit()

    def load(self,s):
        def as_breakpoint(d):
            if 'enabled' in d:
                return Breakpoint(d)
            return d
        try:
            all=json.loads(s,object_hook=as_breakpoint)
            self.breakpoints={}
            for path in all:
                bps=all.get(path)
                self.pathBreakpoints(path).extend(bps)
            self.breakpointsChanged.emit()
        except ValueError:
            print "Failed to load breakpoints from: '{}'".format(s)

    def save(self):
        todel=[]
        for path in self.breakpoints:
            bps=self.breakpoints.get(path)
            if not bps:
                todel.append(path)
        for path in todel:
            del self.breakpoints[path]
        s=BreakpointEncoder().encode(self.breakpoints)
        return s


class BreakpointDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(BreakpointDialog,self).__init__(parent)
        uis.loadDialog('breakpoint',self)
    
    
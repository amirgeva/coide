from PyQt4 import QtCore, QtGui
import uis
import json

class Breakpoint:
    def __init__(self,data=None):
        if data:
            self.data=data
        else:
            self.data={
                'enabled':True,
                'index':-1,
                'condition':''
            }
    
    def condition(self):
        return self.data.get('condition')
        
    def setCondition(self,s):
        self.data['condition']=s
        
    def isEnabled(self):
        return self.data.get('enabled')
    
    def enable(self):
        self.data['enabled']=True
        
    def disable(self):
        self.data['enabled']=False
        
    def save(self):
        return json.dumps(self.data)
        
    def load(self,s):
        self.data=json.loads(s)

class BreakpointEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Breakpoint):
            return obj.data
        return json.JSONEncoder.default(self, obj)

class BreakpointsDB(QtCore.QObject):
    
    breakpointsChanged = QtCore.pyqtSignal()
    
    def __init__(self):
        super(BreakpointsDB,self).__init__()
        self.breakpoints={}
        
    def clear(self):
        self.breakpoints.clear()
        
    def printall(self):
        print self.breakpoints
        
    def paths(self):
        return self.breakpoints.keys()
        
    def pathBreakpoints(self,path):
        if not path in self.breakpoints:
            self.breakpoints[path]={}
        return self.breakpoints.get(path)
        
    def setBreakpoint(self,path,line,enabled):
        bps=self.pathBreakpoints(path)
        bps[line]=Breakpoint()
        if not enabled:
            bps.get(line).disable()
        self.breakpointsChanged.emit()
        
    def removeBreakpoint(self,path,line):
        bps=self.pathBreakpoints(path)
        del bps[line]
        self.breakpointsChanged.emit()
        
    def getBreakpoint(self,path,line):
        return self.pathBreakpoints(path).get(line)
        
    def hasBreakpoint(self,path,line):
        if not path in self.breakpoints:
            return False
        bps=self.pathBreakpoints(path)
        return line in bps
        
    def toggleBreakpoint(self,path,line):
        bps=self.pathBreakpoints(path)
        if line in bps:
            del bps[line]
        else:
            bps[line]=Breakpoint()
        self.breakpointsChanged.emit()

    def loadOld(self,s):        
        self.breakpoints={}
        if len(s)>0:
            srcinfos=s.split(';')
            for src in srcinfos:
                if len(src)>0:
                    fields=src.split(',')
                    path=fields[0]
                    del fields[0]
                    n=len(fields)
                    for i in xrange(0,(n/2)):
                        line=int(fields[i*2])
                        enabled=(fields[i*2+1]=='1')
                        bps=self.pathBreakpoints(path)
                        bps[line]=Breakpoint(enabled)
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
                dst=self.pathBreakpoints(path)
                for line in bps:
                    dst[int(line)]=bps.get(line)
            self.breakpointsChanged.emit()
        except ValueError:
            print "Failed to load breakpoints from: '{}'".format(s)

    def save(self):
        s=BreakpointEncoder().encode(self.breakpoints)
        return s

    def saveOld(self):
        arr=[]
        for path in self.breakpoints:
            arr.append(path)
            bps=self.breakpoints.get(path)
            for line in bps.keys():
                bp=bps[line]
                arr.append(',')
                arr.append(str(line))
                arr.append(',')
                arr.append('1' if bp.enabled else '0')
            arr.append(';')
        return ''.join(arr)


class BreakpointDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(BreakpointDialog,self).__init__(parent)
        uis.loadDialog('breakpoint',self)
    
    
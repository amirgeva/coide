from PyQt4 import QtCore

class Breakpoint:
    def __init__(self,enabled=True,index=-1):
        self.enabled=enabled
        self.index=index

class BreakpointsDB(QtCore.QObject):
    
    breakpointsChanged = QtCore.pyqtSignal()
    
    def __init__(self):
        super(BreakpointsDB,self).__init__()
        self.breakpoints={}
        
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
        bps[line]=Breakpoint(enabled)
        self.breakpointsChanged.emit()
        
    def removeBreakpoint(self,path,line):
        bps=self.pathBreakpoints(path)
        del bps[line]
        self.breakpointsChanged.emit()
        
    def toggleBreakpoint(self,path,line):
        bps=self.pathBreakpoints(path)
        if line in bps:
            del bps[line]
        else:
            bps[line]=Breakpoint()
        self.breakpointsChanged.emit()

    def load(self,s):        
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

    def save(self):
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
        
        
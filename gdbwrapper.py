from PyQt4 import QtCore
from PyQt4 import QtGui
import subprocess
import re
import fcntl
import os
import inspect
import imp
import sys
import time
import parseutils

class GDBWrapper:
    """ Wrapper above the GDB process

    Use subprocess.Popen methods to communicate with gdb.  Write commands
    and read/parse responses    
    
    """

    def __init__(self,bps,args):
        """ Start gdb.  dataRoot indicates location of parsers """
        self.breakpoints=bps
        dataRoot=os.path.dirname(os.path.abspath(__file__))
        #print "Starting debugger for: {}".format(args)
        self.args=['gdb']+args
        self.debugged=os.path.abspath(args[0])
        self.dumpLog=None
        # During development create a dump log
        if len(os.getenv('COIDE',''))>0:
            self.dumpLog=open('dump.log','w')
        self.initializeParsers(os.path.join(dataRoot,"parsers"))
        self.gdb=subprocess.Popen(self.args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        fcntl.fcntl(self.gdb.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        
        self.outputFileName="/tmp/{}.coide".format(int(time.time()))
        self.outputFile=None
        self.outputText=[]
        
        # re for finding location pattern in backtrace
        #       #0  print_str (s=...) at /home/user/main.cpp:42
        self.btPattern=re.compile('at (.+):(\d+)')
        self.curPattern=re.compile('File (.+):\n')
        self.pathPattern=re.compile('(/.+)+')
        self.locPattern=re.compile('Located in (.+)$')
        # Read the gdb startup text
        self.read()

        self.running=False   # Indicates the debugged program has started
        self.active=False    # Program is currenly running, debugger waiting for breakpoint or exit
        self.changed=True
        # dict:  str filepath -> dict of breakpoints ( int line -> Breakpoint )
        self.allFiles=set()
        self.initializePrettyPrints(dataRoot)
        self.recursiveTypes={'map','vector','struct'}
        
        self.pid=''
                     
        self.write('start > {}'.format(self.outputFileName))
        self.read()
        self.write('info inferior')
        lines,ok=self.read()
        if ok:
            for line in lines:
                m=re.match('\*\s+\d+\s+process\s+(\d+)',line)
                if not m is None:
                    g=m.groups()
                    self.pid=g[0]
                    self.running=True
        if len(self.pid)==0:
            QtGui.QMessageBox.critical(self,'Problem','Failed to get debugged program PID')
        self.setBreakpoints()
        self.outputFile=os.open(self.outputFileName,os.O_RDONLY | os.O_NONBLOCK)

    def initializePrettyPrints(self,dataRoot):
        """ Installs the python extension for pretty printing """
        path=os.path.join(dataRoot,"gdb_printers","python")
        cmd=("python\nimport sys\nsys.path.insert(0,'{}')\n"+
            "from libstdcxx.v6.printers import register_libstdcxx_printers\n"+
            "register_libstdcxx_printers(None)\nend").format(path)
        self.write(cmd)
        lines,ok=self.read()
        if not ok:
            print "Failed to install pretty prints"

    def quitDebugger(self):
        #print "Closing debugger"
        if self.active:
            self.actBreak()
        if self.running:
            self.actStop()
        self.write('quit')
        self.gdb.wait()
        if self.outputFile:
            os.close(self.outputFile)
            self.outputFile=None
        os.remove(self.outputFileName)
        
    def closingApp(self):
        """ Called before the application window is closed
        
        Performs cleanup by optionally breaking and killing the program's
        process.
        Quits and waits for gdb to exit
        
        """
        self.quitDebugger()

    def update(self):
        """ Polls the gdb to see if it stopped at a breakpoint or finished """
        if self.outputFile:
            s=os.read(self.outputFile,1024)
            if len(s)>0:
                self.outputText.append(s)
        if self.active:
            lines,ok=self.read(1)
            if ok:
                for line in lines:
                    if line.find('exited normally')>0:
                        self.running=False
                self.active=False
                return ''
            #return lines
        return ''
        
    def hasOutput(self):
        return len(self.outputText)>0
        
    def getOutput(self):
        s=''.join(self.outputText)
        self.outputText=[]
        return s

    def getBackTrace(self):
        if self.active:
            return []
        self.write('bt')
        lines,ok=self.read()
        if not ok:
            return []
        return lines

    def isValidSource(self,cand):
        """ Checks if a string looks like a valid source file
        
        Assumes /usr/* files are library files that should not be included
        in the source files list.
        
        """
        
        if cand.startswith('/usr'):
            return False
        if cand.find('built-in')>0:
            return False
        validExts={'.c','.cpp','.cxx','.C','.cc'}
        for e in validExts:
            if cand.endswith(e):
                return True
        return False
        
    def getAllFiles(self):
        """ Queries all source files and returns a list of valid files """
        files=set()
        self.write("info sources")
        lines,ok=self.read()
        if not ok:
            return []
        for line in lines:
            comps=line.strip().split(',')
            for cand in comps:
                cand=cand.strip()
                if self.isValidSource(cand):
                    files|={cand}
        self.allFiles=files
        return sorted(list(files))
        
    def updateBreakpoints(self):
        """ Queries and updates the breakpoints dict """
        if not self.active:
            allBps={}
            self.write('info break')
            lines,ok=self.read()
            if ok:
                n=len(lines)
                for i in xrange(0,n):
                    parts=lines[i].split()
                    if parts[1]=='breakpoint':
                        index=int(parts[0])
                        enabled=(parts[3]=='y')
                        if parts[-2]=='at':
                            parts=parts[-1].split(':')
                        else:
                            parts=lines[i+1].strip().split()
                            parts=parts[-1].split(':')
                        path=parts[0]
                        line=int(parts[1])
                        self.log("{}: ({}) Breakpoint '{}':{}".format(index,enabled,path,line))
                        if not allBps.has_key(path):
                            allBps[path]={}
                        bps=allBps.get(path)
                        bps[line]=Breakpoint(enabled,index)
                self.breakpoints.loadFeedback(allBps)

    
    def updatePath(self,name):
        """ Given a file name, find the first file path that matches """
        if name[0]=='/':
            return name
        for f in self.allFiles:
            if f.endswith(name):
                return f
        return name                        
        
    def getCurrentPos(self):
        """ Queries the current file,line and return them
        
        If none can be found, returns an empty path
        
        """
        res="","1"
        if self.running:
            self.write("bt")
            lines,ok=self.read()
            if ok:
                self.changed=False
                ml='\n'.join(lines)
                m=re.search(self.btPattern,ml)
                if not m is None:
                    g=m.groups()
                    path=self.updatePath(g[0])
                    res=(path,g[1])
            self.write("info source")
            lines,ok=self.read()
            if ok:
                for line in lines:
                    m=re.match(self.locPattern,line)
                    if not m is None:
                        g=m.groups()
                        res=(g[0],res[1])
                        break
        else:
            self.write("info function main")
            lines,ok=self.read()
            if ok:
                self.changed=False
                ml='\n'.join(lines)
                m=re.search(self.curPattern,ml)
                if not m is None:
                    path=self.updatePath((m.groups())[0])
                    res=(path,"1")
        return (res[0],int(res[1]))
        
    def log(self,s):
        """ Logs text during development (DEBUGUI env var) """
        if not self.dumpLog is None:
            self.dumpLog.write(s)
            self.dumpLog.write('\n')
            self.dumpLog.flush()
        
    def write(self,s):
        """ Writes a command to the gdb stdin """
        self.log('>{}'.format(s))
        self.gdb.stdin.write(s+'\n')
    
    def read(self,tries=100):
        """ Reads response lines from the gdb stdout
        
        tries indicates number of times to poll until the (gdb) prompt
        is encountered.  Each failed try waits for 10ms
        
        """
        res=""
        count=0
        while count<tries:
            try:
                count+=1
                l=self.gdb.stdout.read()
                res+=l
                if res.endswith('(gdb) '):
                    self.changed=True
                    res=res.split('\n')
                    del res[-1]
                    self.log('<<{}'.format('\n'.join(res)))
                    return (res,True)
            except IOError:
                time.sleep(0.01)
        return (res,False)
        
    def clearBreakpoints(self):
        self.write("set confirm off")
        self.read()
        self.write("delete")
        self.read()
        
    #def getBreakpoints(self,path):
    #    if not self.breakpoints.has_key(path):
    #        name=os.path.basename(path)
    #        if not self.breakpoints.has_key(name):
    #            return {}
    #        return self.breakpoints.get(name)
    #    return self.breakpoints.get(path)
    
    def setBreakpoint(self,path,line):    
        self.write('break {}:{}'.format(path,line))
        self.read()
        self.changed=True
    
    def toggleBreakpoint(self,path,line):
        if not self.active:
            self.log("Toggling breakpoint at '{}' : {}".format(path,line))
            self.write('clear {}:{}'.format(path,line))
            lines,ok=self.read()
            if not ok:
                return
            resp=''.join(lines)
            self.log("clear resp='{}'".format(resp))
            if resp.find('Deleted breakpoint')<0:
                self.write('break {}:{}'.format(path,line))
                self.read()
            self.changed=True
    
    def ableBreakpoint(self,path,line):
        """ Enables/Disables a breakpoint """
        if not self.active and self.breakpoints.has_key(path):
            bps=self.breakpoints[path]
            if bps.has_key(line):
                self.log("Abling breakpoint at '{}' : {}".format(path,line))
                bp=bps[line]
                if bp.enabled:
                    self.write('disable {}'.format(bp.index))
                else:
                    self.write('enable {}'.format(bp.index))
                lines,ok=self.read()
                if ok:
                    bp.enabled=not bp.enabled

    def setBreakpoints(self):
        self.clearBreakpoints()
        for path in self.breakpoints.paths():
            bps=self.breakpoints.pathBreakpoints(path)
            for line in bps:
                bp=bps.get(line)
                line=line+1
                self.setBreakpoint(path,line)
                if not bp.enabled:
                    self.ableBreakpoint(path,line)
    
    def actStep(self):
        """ Single steps going into function calls """
        if not self.active and self.running:
            self.write('step')
            lines,ok=self.read()

    def actNext(self):
        """ Single steps going over function calls """
        if not self.active and self.running:
            self.write('next')
            lines,ok=self.read()
            if not ok:
                self.active=True

    def actOut(self):
        """ Executes until current function (stack frame) ends """
        if not self.active:
            self.write('finish')
            lines,ok=self.read()
            if not ok:
                self.active=True

    def actCont(self):
        """ Continue running the program (until done, or breakpoint) """
        if not self.running:
            self.write('run')
            self.running=True
            self.active=True
        else:
            self.write('cont')
            self.active=True
            
    def actBreak(self):
        """ Breaks a running program by sending it a SIGINT """
        if self.active and len(self.pid)>0:
            subprocess.call(['kill','-s','SIGINT',self.pid])
            lines,ok=self.read(200)
            if ok:
                self.active=False
            else:
                self.log("Break Failed")
                print "Failed to break gdb"
            self.changed=True

    def actStop(self):
        """ Kills the program's process and terminates debugging """
        if self.active:
            self.actBreak()
        if not self.active:
            self.write('kill')
            time.sleep(0.1)
            self.write('y')
            lines,ok=self.read()
            if ok:
                self.running=False

    def initializeParsers(self,parsersDir):
        """ Search and load all found parser source (py) files """
        self.parsers={}
        self.replaces={}
        try:
            files=os.listdir(parsersDir)
        except OSError:
            dir=os.path.join(sys.prefix,'share/debugui')
            if parsersDir!=dir:
                self.initializeParsers(dir)
            return
        for f in files:
            if f.endswith('.py'):
                try:
                    name=(os.path.splitext(f))[0]
                    mod=imp.load_source(name,os.path.join(parsersDir,f))
                    funcs=inspect.getmembers(mod,predicate=inspect.isroutine)
                    found=0
                    for func in funcs:
                        if func[0]=='parse':
                            self.parsers[name]=func[1]
                            found+=1
                        if func[0]=='replaces':
                            fn=func[1]
                            self.replaces.update(fn())
                            found+=1
                    #if found>0:
                    #    print "Loaded parser {}".format(name)
                except ImportError:
                    pass

    def recursiveParse(self,l):
        """ For complex types, parses the value of a subtree """
        n=len(l)
        if n==2 and l[0] in self.recursiveTypes:
            for i in xrange(0,n):
                child=l[i]
                if type(child) is list:
                    self.recursiveParse(child)
                else:
                    pr=self.parsePrintout(child)
                    if len(pr)>0:
                        l[i]=pr

    def parsePrintout(self,text):
        """ Parses the evaluated value of expressions """
        text=parseutils.removeVar(text)
        text=parseutils.removeRef(text)
        for parser in self.parsers.keys():
            func=self.parsers.get(parser)
            res=func(text)
            self.recursiveParse(res)
            if len(res)>0:
                return res
        return []
        
    def evaluate(self,var):
        """ Evaluates the value of expression """
        if self.active or not self.running:
            return ''
        ch=self.changed
        self.write('print {}'.format(var))
        lines,ok=self.read()
        self.changed=ch
        if not ok: 
            #print "Failed to evaluate {}".format(var)
            return ''
        #print '{} = {}'.format(var,lines)
        if type(lines) is list:
            lines='\n'.join(lines)
        while lines.find('  ')>=0:
            lines=lines.replace('  ',' ')
        for k in self.replaces.keys():
            lines=lines.replace(k,self.replaces.get(k))
        self.log("Parsing:\n"+lines)
        res=self.parsePrintout(lines)
        self.log(str(res))
        return res
            
    


if __name__ == '__main__':
    s='$7 = {name = "Check", value = 45}'
    print sys.argv[0]
    d=GDBWrapper('.',['tst'])
    res=d.parsePrintout(s)
    print res

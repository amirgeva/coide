from PyQt4 import QtCore
from PyQt4 import QtGui
import subprocess
import re
import fcntl
import os
import time
import handlers
import globals

class GDBWrapper:
    """ Wrapper above the GDB process

    Use subprocess.Popen methods to communicate with gdb.  Write commands
    and read/parse responses    
    
    """

    def __init__(self,bps,args,dir):
        """ Start gdb. """
        settings=QtCore.QSettings()
        self.breakpoints=bps
        self.breakpoints.breakpointsChanged.connect(self.setBreakpoints)
        dataRoot=os.path.dirname(os.path.abspath(__file__))
        #print "Starting debugger for: {}".format(args)
        self.args=['gdb','--args']+args
        self.debugged=os.path.abspath(args[0])
        arglist=''
        if len(args)>1:
            for i in xrange(1,len(args)):
                arglist=arglist+' "{}"'.format(args[i])
        self.dumpLog=None
        # During development create a dump log
        if len(os.getenv('COIDE',''))>0:
            self.parseCount=0
            self.dumpLog=open('dump.log','w')
        self.initHandlers()
        self.gdb=subprocess.Popen(self.args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
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
        time.sleep(10)
        lines,ok=self.read()

        # Wait for GDB to complete init
        if False:
            bla_index=0
            while True:
                s='BLA{}'.format(bla_index)
                self.write(s)
                lines,ok=self.read()
                if s in lines:
                    break
                bla_index+=1
                time.sleep(1)


        self.running=False   # Indicates the debugged program has started
        self.active=False    # Program is currenly running, debugger waiting for breakpoint or exit
        self.changed=True
        # dict:  str filepath -> dict of breakpoints ( int line -> Breakpoint )
        self.allFiles=set()
        
        if settings.value('customPrinters',True).toBool():
            self.initializePrettyPrints(dataRoot)
        
        self.pid=''

        self.write('start {} > {}'.format(arglist,self.outputFileName))
        lines, ok =self.read()
        if globals.dev:
            print lines
        self.write('info inferior')
        lines,ok=self.read()
        if ok:
            for line in lines:
                print line
                m=re.match('\*\s+\d+\s+process\s+(\d+)',line)
                if not m is None:
                    g=m.groups()
                    self.pid=g[0]
                    self.running=True
        if len(self.pid)==0:
            QtGui.QMessageBox.critical(None,'Problem','Failed to get debugged program PID')
        self.setBreakpoints()
        self.outputFile=os.open(self.outputFileName,os.O_RDONLY | os.O_NONBLOCK)
        
    def initHandlers(self):
        self.handlers=[]
        self.handlers.append(handlers.SignalHandler())

    def initializePrettyPrints(self,dataRoot):
        """ Installs the python extension for pretty printing """
        path=os.path.join(dataRoot,"gdb_printers","python")
        cmd=("python\nimport sys\nsys.path.insert(0,'{}')\n"+
#            "from libstdcxx.v6.printers import register_libstdcxx_printers\n"+
#            "from prims.printers import register_prim_printers\n"+
#            "register_libstdcxx_printers(None)\n"+
#            "register_prim_printers()\n"+
            "from eigen.printers import register_eigen_printers\n"+
            "register_eigen_printers(None)\n"+
            "end").format(path)
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
        self.gdb=None
        
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
            #if ok:
            #    for line in lines:
            #        if line.find('exited normally')>0:
            #            self.running=False
            #    self.active=False
            #    return ''
            #return lines
        return ''
        
    def sendInput(self,s):
        self.gdb.stdin.write(s)
        
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
        res=[("","1")]
        if self.running:
            self.write("bt")
            lines,ok=self.read()
            if ok:
                self.changed=False
                ml='\n'.join(lines)
                m=re.findall(self.btPattern,ml)
                if not m is None:
                    res=[]
                    for i in range(0,len(m)):
                        r=m[i]
                        res.append((self.updatePath(r[0]),int(r[1])))
            #self.write("info source")
            #lines,ok=self.read()
            #if ok:
            #    for line in lines:
            #        m=re.match(self.locPattern,line)
            #        if not m is None:
            #            g=m.groups()
            #            res=[(g[0],int(g[1]))]
            #            break
        else:
            self.write("info function main")
            lines,ok=self.read()
            if ok:
                self.changed=False
                ml='\n'.join(lines)
                m=re.search(self.curPattern,ml)
                if not m is None:
                    path=self.updatePath((m.groups())[0])
                    res=[(path,1)]
        return res
        
    def log(self,s):
        """ Logs text during development (DEBUGUI env var) """
        if not self.dumpLog is None:
            self.dumpLog.write(s)
            self.dumpLog.write('\n')
            self.dumpLog.flush()
        
    def write(self,s):
        """ Writes a command to the gdb stdin """
        if globals.dev:
            print '>{}'.format(s)
        self.log('>{}'.format(s))
        self.gdb.stdin.write(s+'\n')
    
    def read(self,tries=100):
        """ Reads response lines from the gdb stdout
        
        tries indicates number of times to poll until the (gdb) prompt
        is encountered.  Each failed try waits for 10ms
        
        """
        res=""
        count=0
        for h in self.handlers:
            h.reset()
        while count<tries:
            try:
                count+=1
                l=self.gdb.stdout.read()
                for h in self.handlers:
                    h.addLine(l)
                res+=l
                if res.endswith('(gdb) '):
                    self.changed=True
                    res=res.split('\n')
                    del res[-1]
                    self.log('<<{}'.format('\n'.join(res)))

                    for line in res:
                        if line.find('exited normally')>0:
                            self.running=False
                    self.active=False
                    if globals.dev:
                        print res
                    return (res,True)
            except IOError:
                time.sleep(0.01)
        return (res,False)
        
    def clearBreakpoints(self):
        self.write("set confirm off")
        self.read()
        self.write("delete")
        self.read()
        
    def setBreakpoint(self,path,line,cond):
        cmd='break {}:{}'.format(path,line)
        if cond:
            cmd=cmd+' if {}'.format(cond)
        self.write(cmd)
        self.read()
        self.changed=True
    
    def setBreakpoints(self):
        if not self.gdb:
            return
        self.clearBreakpoints()
        for path in self.breakpoints.paths():
            bps=self.breakpoints.pathBreakpoints(path)
            for bp in bps:
                if bp.isEnabled():
                    line=bp.line()+1
                    self.setBreakpoint(path,line,bp.condition())
    
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
        
    def printVar(self,var):        
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
        return lines
        
    def evaluate(self,var):
        import xparse
        lines=self.printVar(var)
        if globals.dev:
            print "@@@\n{}\n@@@".format(lines)
        return xparse.parse(lines)
        
    def flatten(self,root):
        if not root:
            return ''
        res=root.value
        if len(root.children)>0:
            res=res+' { '
            index=0
            for c in root.children:
                if index>0:
                    res=res+', '
                res=res+self.flatten(c)
                index=index+1
            res=res+' } '
        return res
        
    def evaluateAsText(self,var):
        root=self.evaluate(var)
        return self.flatten(root)

    def getVarsInfo(self,vartype,res):
        if self.active or not self.running:
            return res
        ch=self.changed
        self.write('info {}'.format(vartype))
        lines,ok=self.read()
        self.changed=ch
        if not ok:
            #print "Failed to evaluate {}".format(var)
            return res
        if type(lines) is list:
            lines='\n'.join(lines)
        lines=lines.split('\n')
        groups=[]
        for line in lines:
            if line:
                if line[0]!=' ':
                    groups.append([])
                groups[-1].append(line)
        for group in groups:
            all='\n'.join(group)
            import xparse
            #from xparse.xparse import Node
            cur=xparse.parse(all)
            if cur:
                res[cur.name]=cur

    def getLocals(self):
        res={}
        self.getVarsInfo('args',res)
        self.getVarsInfo('locals',res)
        return res
        


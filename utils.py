import os
import time
import subprocess
import select
from PyQt4 import QtGui

iconsDir='.'

def timestamp(title):
    #print "{}: {}".format(int(round(time.time()*1000)),title)
    pass

def setIconsDir(dir):
    global iconsDir
    iconsDir=dir
    
def loadIcon(name):
    if not name.endswith('.png'):
        name=name+".png"
    path=os.path.join(iconsDir,name)
    icon=QtGui.QIcon(path)
    return icon

def message(msg):
    m=QtGui.QMessageBox()
    m.setText(msg)
    m.exec_()

def errorMessage(msg):
    message(msg)

# Find the dependency on a header in a makefile 
# and return an object path that depends on it
def objForHeader(mkPath,headerPath):
    for line in open(mkPath,'r').readlines():
        p=line.strip().split()
        if len(p)==0:
            continue
        p0=p[0]
        if p0.endswith('.o:') and '/Debug/' in p0:
            o=p0[0:-1]
            if headerPath in p:
                return o
    return ''

def appendOutput(output,text):
    #text=output.toPlainText()
    #output.setPlainText(text+added)
    #c=output.textCursor()
    #c.movePosition(QtGui.QTextCursor.End)
    #output.setTextCursor(c)
    #output.ensureCursorVisible()
    output.appendLine(text)

def appendColorLine(output,line,color):
    line=line.decode('utf8')
    c=output.textCursor()
    c.movePosition(QtGui.QTextCursor.End)
    f=c.charFormat()
    f.setForeground(QtGui.QBrush(QtGui.QColor(color)))
    c.setCharFormat(f)
    output.setTextCursor(c)
    output.appendLine(line)
    

def appendLine(output,line):
    if line.find('Nothing to be done for')>0:
        return
    if line!='':
        parts=line.split(' ')
        color='#000000'
        if len(parts)>2 and parts[1]=='-c':
            line='Compiling '+parts[-1]
            color='#000080'
        elif line.startswith('ar cr '):
            libname=(parts[2].split('/'))[-1]
            line='Creating library {}'.format(libname)
            color='#000080'
        elif line.startswith('g++ -o'):
            appname=(parts[2].split('/'))[-1]
            line='Linking {}'.format(appname)
            color='#000080'
        elif parts[0]=='cppcheck':
            return
        lower=line.lower()
        if lower.find('error')>0:
            appendColorLine(output,line,'#ff0000')
        else:
            appendColorLine(output,line,color)

def checkFor(cmd):
    try:
        res=subprocess.call(['which',cmd],stdout=open('/dev/null','w'))
        return res==0
    except OSError:
        return False

def runcmd(dir,cmdlist,pipes=True):
    if pipes:
        return subprocess.Popen(cmdlist, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=dir)
    return subprocess.Popen(cmdlist, shell=False, cwd=dir)
    
def run(dir,cmd,*args):
    return runcmd(dir,[cmd]+list(args),False)

def call(dir,cmd,*args):
    return runcmd(dir,[cmd]+list(args)).communicate('')

def shellrun(dir,cmd):
    return subprocess.Popen(['-c',cmd],shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
    
def shellcall(dir,cmd):
    return shellrun(dir,cmd).communicate()

class AsyncExecute:
    def __init__(self,output,dir,cmdlist):
        self.output=output
        self.pdone=False
        self.text=[]
        self.act=1
        self.cmdlist=cmdlist
        self.rc=None
        self.process=subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
        
    def poll(self):
        if self.pdone and self.act==0:
            return True
        reads=[self.process.stdout.fileno(),self.process.stderr.fileno()]
        self.act=0
        rc=select.select(reads,[],[],0)
        for fd in rc[0]:
            if fd==self.process.stdout.fileno():
                line=self.process.stdout.readline().strip()
                appendLine(self.output,line)
                self.text.append(line)
                if len(line)>0:
                    self.act=self.act+1
            if fd==self.process.stderr.fileno():
                line=self.process.stderr.readline().strip()
                appendLine(self.output,line)
                self.text.append(line)
                if len(line)>0:
                    self.act=self.act+1
        if self.process.poll()!=None:
            self.rc=self.process.returncode
            self.pdone=True
        if self.pdone and self.act==0:
            return True
        return False

async_executes=[]

def pendingAsync():
    if len(async_executes)>0:
        print "Pending: {}".format(async_executes[0].cmdlist)
        return True
    return False

def execute(output,dir,cmd,*args):
    cmdlist=[cmd]+list(args)
    ae=AsyncExecute(output,dir,cmdlist)
    async_executes.append(ae)
    return ae
    
def pollAsync():
    res=[]
    n=len(async_executes)
    for i in xrange(0,n):
        ae=async_executes[i]
        if ae.poll():
            res.append(async_executes[i].rc)
            del async_executes[i]
            return res+pollAsync()
    return res
        

def old_execute(output,dir,cmd,*args):
    output.clear()
    cmdlist=[cmd]+list(args)
    text=[]
    pdone=False
    act=1
    p = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
    while not pdone or act>0:
        reads=[p.stdout.fileno(),p.stderr.fileno()]
        act=0
        rc=select.select(reads,[],[])
        for fd in rc[0]:
            if fd==p.stdout.fileno():
                line=p.stdout.readline().strip()
                appendLine(output,line)
                text.append(line)
                if len(line)>0:
                    act=act+1
            if fd==p.stderr.fileno():
                line=p.stderr.readline().strip()
                appendLine(output,line)
                text.append(line)
                if len(line)>0:
                    act=act+1
        if p.poll()!=None:
            pdone=True
        else:
            time.sleep(0.05)
    return text

def findLine(path,prefix,removePrefix=False):
    f=open(path,"r")
    for line in f:
        if line.startswith(prefix):
            line=line.strip()
            if not removePrefix:
                return line
            return line[len(prefix):]
    return ''
       
def browseDirectory(lineedit):
    cur=lineedit.text()
    cur=QtGui.QFileDialog.getExistingDirectory(caption="Working Directory",directory=cur)
    if cur:
        lineedit.setText(cur)

def setCheckbox(cb,on):
    cb.setCheckState(QtCore.Qt.Checked if on else QtCore.Qt.Unchecked)
    
def getCheckbox(cb):
    return cb.checkState()==QtCore.Qt.Checked


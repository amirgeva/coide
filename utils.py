import os
import time
import subprocess
import select
#from PyQt4 import QtCore
from PyQt4 import QtGui

iconsDir='.'

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


def appendOutput(output,text):
    #text=output.toPlainText()
    #output.setPlainText(text+added)
    #c=output.textCursor()
    #c.movePosition(QtGui.QTextCursor.End)
    #output.setTextCursor(c)
    #output.ensureCursorVisible()
    output.appendPlainText(text)

def appendColorLine(output,line,color):
    line=line.decode('utf8')
    c=output.textCursor()
    c.movePosition(QtGui.QTextCursor.End)
    f=c.charFormat()
    f.setForeground(QtGui.QBrush(QtGui.QColor(color)))
    c.setCharFormat(f)
    output.setTextCursor(c)
    output.appendPlainText(line)
    

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
        lower=line.lower()
        if lower.find('error')>0:
            appendColorLine(output,line,'#ff0000')
        else:
            appendColorLine(output,line,color)

def runcmd(dir,cmdlist):
    return subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
    
def run(dir,cmd,*args):
    return runcmd(dir,[cmd]+list(args))

def call(dir,cmd,*args):
    return runcmd(dir,[cmd]+list(args)).communicate()

class AsyncExecute:
    def __init__(self,output,dir,cmdlist):
        self.output=output
        self.pdone=False
        self.text=[]
        self.act=1
        self.process=subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
        
    def poll(self):
        if self.pdone and self.act==0:
            return True
        reads=[self.process.stdout.fileno(),self.process.stderr.fileno()]
        self.act=0
        rc=select.select(reads,[],[])
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
            self.pdone=True
        if self.pdone and self.act==0:
            return True
        return False

async_executes=[]
        
def execute(output,dir,cmd,*args):
    cmdlist=[cmd]+list(args)
    async_executes.append(AsyncExecute(output,dir,cmdlist))
    
def pollAsync():
    n=len(async_executes)
    for i in xrange(0,n):
        ae=async_executes[i]
        if ae.poll():
            del async_executes[i]
            return pollAsync()
    return n>0
        

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
       

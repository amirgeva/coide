import os
import sys
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
    #print "Loading '{}'".format(path)
    return QtGui.QIcon(path)

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
    
def execute(output,dir,cmd,*args):
    output.clear()
    cmdlist=[cmd]+list(args)
    text=[]
    p = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
    while True:
        reads=[p.stdout.fileno(),p.stderr.fileno()]
        rc=select.select(reads,[],[])
        for fd in rc[0]:
            if fd==p.stdout.fileno():
                line=p.stdout.readline().strip()
                appendLine(output,line)
                text.append(line)
            if fd==p.stderr.fileno():
                line=p.stderr.readline().strip()
                appendLine(output,line)
                text.append(line)
        if p.poll() != None:
            break
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
    
    
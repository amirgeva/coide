import os
import sys
import subprocess
import select
#from PyQt4 import QtCore
from PyQt4 import QtGui


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
    c=output.textCursor()
    c.movePosition(QtGui.QTextCursor.End)
    f=c.charFormat()
    f.setForeground(QtGui.QBrush(QtGui.QColor(color)))
    c.setCharFormat(f)
    output.setTextCursor(c)
    output.appendPlainText(line)
    

def appendLine(output,line):
    if line!='':
        parts=line.split(' ')
        color='#000000'
        if len(parts)>2 and parts[1]=='-c':
            line='Compiling '+parts[-1]
            color='#000080'
        lower=line.lower()
        if lower.find('error')>0:
            appendColorLine(output,line,'#ff0000')
        else:
            appendColorLine(output,line,color)

def execute(output,dir,cmd,*args):
    p = subprocess.Popen([cmd]+list(args), shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=dir)
    while True:
        reads=[p.stdout.fileno(),p.stderr.fileno()]
        rc=select.select(reads,[],[])
        for fd in rc[0]:
            if fd==p.stdout.fileno():
                appendLine(output,p.stdout.readline().strip())
            if fd==p.stderr.fileno():
                appendLine(output,p.stderr.readline().strip())
        if p.poll() != None:
            break

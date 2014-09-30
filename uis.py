#!/usr/bin/env python
import os
from subprocess import call
from PyQt4 import QtGui
import re
import inspect
import importlib

def loadDialog(name,dlg=None):
    module=importlib.import_module('gen.'+name)
    for name,obj in inspect.getmembers(module):
        if name.startswith("Ui_"):
            if not dlg:
                dlg=QtGui.QDialog()
            ui=obj()
            ui.setupUi(dlg)
            return dlg


def generate():
    inputs = os.listdir('uis')
    for uiName in inputs:
        base=(os.path.splitext(uiName))[0]
        inpath=os.path.join('uis',uiName)
        outpath=os.path.join('gen',base+".py")
        call(['pyuic4','-o',outpath,inpath])
        dlg='dlg'
        f=open(outpath,"r")
        lines=f.readlines()
        f.close()
        for i in xrange(0,len(lines)):
            line=lines[i]
            if line.startswith("class Ui_"):
                dlg=(re.split('\W+',line))[1]
                dlg=dlg[3:]
            p=line.find('self.')
            if p>0:
                sym=line[p+5:]
                if not sym.startswith('retranslateUi'):
                    lines[i]=line.replace('self.',dlg+'.')
        f=open(outpath,"w")
        f.write(''.join(lines))
        f.close()
        #call(['sed','-i','s/self\\.\\([^retranslateUi]\\)/{}.\\1/g'.format(dlg),outpath])
        
if __name__=='__main__':
    generate()

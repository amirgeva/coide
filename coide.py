#!/usr/bin/env python
import sys
import os

import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore
from PyQt4 import QtGui
#from gdbwrapper import GDBWrapper
from mainwindow import MainWindow
import callbacks

def main():
    """ Creates the main window and runs the application
    
    In package deployment, root usually gets a value of:
    /usr/share/debugui
    (depending on sys.prefix)
    
    For development, use the DEBUGUI env var to indicate the 
    directory where the 'parsers' and 'icons' sub-dirs are
    
    """

    app=QtGui.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("MLGSoft")
    QtCore.QCoreApplication.setOrganizationDomain("mlgsoft.com")
    QtCore.QCoreApplication.setApplicationName("Coide")
    root=os.getenv('COIDE','')
    if len(root)==0:
        root=os.path.join(sys.prefix,"share/coide")
    if not os.path.exists(os.path.join(root,"parsers")):
        root=os.path.dirname(os.path.realpath(__file__))
    #dbg=GDBWrapper(root,sys.argv[1:])
    w=MainWindow(root)
    #w.setDebugger(dbg)
    w.show()
    app.exec_()
    for cb in callbacks.closeCallbacks:
        cb()

if __name__=='__main__':
    main()
    

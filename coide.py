#!/usr/bin/env python
import sys
import os

try:
    import sip
    sip.setapi('QString', 2)
except ImportError:
    print "sip not installed.  try:   sudo apt-get install python-sip"
    sys.exit(1)

try:
    from PyQt4 import QtCore
    from PyQt4 import QtGui
except ImportError:
    print "PyQt4 not installed.  try:   sudo apt-get install python-qt4"
    sys.exit(1)

import globals    
from mainwindow import MainWindow
import callbacks

version = '1.20160121'

def migrateSettings(oldver):
    print "Migrating settings from {} to {}".format(oldver,version)

def checkVersion():
    s=QtCore.QSettings()
    sver=s.value('version','').toString()
    if sver!=version:
        migrateSettings(sver)
        s.setValue('version',version)
        s.sync()

def main():
    """ Creates the main window and runs the application
    
    For development, use the COIDE env var to override the 
    directory where the 'parsers' and 'icons' sub-dirs are
    
    """
    app=QtGui.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("MLGSoft")
    QtCore.QCoreApplication.setOrganizationDomain("mlgsoft.com")
    QtCore.QCoreApplication.setApplicationName("Coide")
    checkVersion()
    root=os.getenv('COIDE','')
    if len(root)==0:
        root=os.path.dirname(os.path.realpath(__file__))
    else:
        globals.dev=True
    os.chdir(root)
    globals.mw=MainWindow(root)
    globals.mw.show()
    app.exec_()
    import system
    if not system.isScannerDone():
        print "Hold on a few seconds..."
    for cb in callbacks.closeCallbacks:
        cb()

if __name__=='__main__':
    main()
    

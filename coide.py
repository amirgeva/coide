#!/usr/bin/env python3
import sys
import os

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    print("PyQt6 not installed.  try:   pip install PyQt6")
    sys.exit(1)

import globals    
from mainwindow import MainWindow
import callbacks

version = '1.20160121'

def migrateSettings(oldver):
    print("Migrating settings from {} to {}".format(oldver,version))

def checkVersion():
    s=QtCore.QSettings()
    sver=s.value('version','')
    if sver!=version:
        migrateSettings(sver)
        s.setValue('version',version)
        s.sync()

def main():
    """ Creates the main window and runs the application
    
    For development, use the COIDE env var to override the 
    directory where the 'parsers' and 'icons' sub-dirs are
    
    """
    app=QtWidgets.QApplication(sys.argv)
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
    app.exec()
    import system
    if not system.isScannerDone():
        print("Hold on a few seconds...")
    for cb in callbacks.closeCallbacks:
        cb()

if __name__=='__main__':
    main()
    

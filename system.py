import utils
import re
from multiprocessing import Process, Queue
import callbacks

def libraryDirs():
    out,err=utils.call('.','ld','--verbose')
    return re.findall('SEARCH_DIR\("=([^"]+)"\);',out)

def listAllPackages():
    res=set()
    all,err=utils.call('.','pkg-config','--list-all')
    lines=all.splitlines()
    for line in lines:
        name=(line.split(' '))[0]
        res.add(name)
    return res

def symbolScan(q,ws):
    import symbolscanner
    q.put(symbolscanner.getLibrarySymbols(ws))

scanq=Queue()    
scannerProcess=None
scanStarted=False
    
def startSymbolScan(workspacePath):
    global scannerProcess
    global scanStarted
    if scanq and not scanStarted:
        scanStarted=True
        scannerProcess=Process(target=symbolScan,args=(scanq,workspacePath))
        scannerProcess.start()
    
libSyms=None
wsSyms=None

def getLibrarySymbols():
    global libSyms
    global wsSyms
    global scannerProcess
    global scanq
    if not libSyms:
        (libSyms,wsSyms)=scanq.get()
        scannerProcess.join()
        scannerProcess=None
        scanq=None
    return libSyms
    
def getWorkspaceSymbols():
    getLibrarySymbols()
    return wsSyms
        
callbacks.closeCallbacks.append(getLibrarySymbols)

if __name__=='__main__':
    getLibrarySymbols()
    
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

noMP=False
scanq=Queue()
workspacePath=''
scannerProcess=None
scanStarted=False
    

libSyms=None
wsSyms=None
wsLibs=None


def startSymbolScan(ws):
    if not noMP:
        global scannerProcess
        global scanStarted
        global workspacePath
        if scanq and not scanStarted:
            scanStarted=True
            workspacePath=ws
            scannerProcess=Process(target=symbolScan,args=(scanq,workspacePath))
            scannerProcess.start()
    else:
        global libSyms
        global wsSyms
        global wsLibs
        import symbolscanner
        (libSyms,wsSyms,wsLibs)=symbolscanner.getLibrarySymbols(workspacePath)
    
def getLibrarySymbols():
    global libSyms
    global wsSyms
    global wsLibs
    global scannerProcess
    global scanq
    if not libSyms:
        (libSyms,wsSyms,wsLibs)=scanq.get()
        scannerProcess.join()
        scannerProcess=None
        scanq.close()
        scanq=None
        import symbolscanner
        symbolscanner.setInitialResults(workspacePath,libSyms,wsSyms,wsLibs)
    return libSyms
    
def getWorkspaceSymbols():
    getLibrarySymbols()
    return wsSyms
        
callbacks.closeCallbacks.append(getLibrarySymbols)

if __name__=='__main__':
    getLibrarySymbols()
    
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

def symbolScan(q):
    import symbolscanner
    q.put(symbolscanner.librarySymbols)

scanq=Queue()
scannerProcess=Process(target=symbolScan,args=(scanq,))
scannerProcess.start()
libSyms=None

def getLibrarySymbols():
    global libSyms
    global scannerProcess
    global scanq
    if scannerProcess:
        libSyms=scanq.get()
        scannerProcess.join()
        scannerProcess=None
        scanq=None
    return libSyms
    
callbacks.closeCallbacks.append(getLibrarySymbols)

if __name__=='__main__':
    querySymbols(True)
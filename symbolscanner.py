from PyQt4 import QtCore
import sys
import os
import re
import utils
from system import listAllPackages, libraryDirs

def baseLibName(f):
    if f.startswith("lib"):
        f=f[3:]
    p=f.find('.')
    if p>0:
        f=f[0:p]
    return f

def isLibraryDir(dir):
    try:
        path=os.path.join(dir,'Makefile')
        for line in open(path):
            s=line.strip()
            if s=='TYPE=LIB':
                return True
    except IOError:
        pass
    return False

class Scanner:
    instance=None

    def __init__(self,ws,libSyms=None,wsSyms=None,wsLibs=None):
        self.ws=ws
        if libSyms and wsSyms and wsLibs:
            self.librarySymbols=libSyms
            self.workspaceSymbols=wsSyms
            self.workspaceLibSyms=wsLibs
        else:
            self.packages=listAllPackages()
            if self.isPackageListChanged():
                self.libraryMap=self.mapLibrariesToPackages()
                self.librarySymbols=self.querySymbols()
                self.saveLists()
                self.libraryMap={}
            else:
                utils.timestamp('load library lists')
                self.loadLists()
                utils.timestamp('Done load')
            self.workspaceLibSyms={}
            self.workspaceSymbols={}
            self.scanWorkspaceSymbols()

    def isPackageListChanged(self):
        s=QtCore.QSettings()
        if s.contains('all_packages'):
            old_packages=s.value('all_packages').toString().split(',')
            return old_packages != self.packages
        return True
        
    def saveLists(self):
        s=QtCore.QSettings()
        s.setValue('all_packages',','.join(self.packages))
        index={}
        for i in xrange(0,len(self.packages)):
            index[self.packages[i]]=i
        all=[]
        for sym in self.librarySymbols:
            refsIdx=[]
            refs=self.librarySymbols.get(sym)
            for r in refs:
                if r in index:
                    refsIdx.append(str(index.get(r)))
                else:
                    refsIdx.append(r)
            all.append(sym+"."+','.join(refsIdx))
        s.setValue('library_symbols',';'.join(all))
        #s.setValue('library_symbols',pickle.dumps(self.librarySymbols))
        s.sync()
        
    def loadLists(self):
        s=QtCore.QSettings()
        utils.timestamp('load from settings')
        ls=s.value('library_symbols').toString()
        utils.timestamp('deserialize')
        #self.librarySymbols=pickle.loads(ls)
        self.librarySymbols={}
        all=ls.split(';')
        for s in all:
            if s:
                pos=s.find('.')
                if pos>0:
                    sym=s[0:pos]
                    refs=s[pos+1:].split(',')
                    rset=set()
                    self.librarySymbols[sym]=rset
                    for r in refs:
                        try:
                            rset.add(self.packages[int(r)])
                        except ValueError:
                            rset.add(r)

    def mapLibrariesToPackages(self):
        libmap={}
        try:
            for package in self.packages:
                out,err=utils.call('.','pkg-config','--libs',package)
                for token in out.split():
                    if token.startswith('-l'):
                        libname='lib{}'.format(token[2:])
                        static=libname+'.a'
                        dynamic=libname+'.so'
                        if not static in libmap:
                            libmap[static]=set()
                        libmap.get(static).add(package)                    
                        if not dynamic in libmap:
                            libmap[dynamic]=set()
                        libmap.get(dynamic).add(package)
        except OSError:
            pass
        return libmap
    
    def parseStatic(self,path,symbols,f):
        (out,err)=utils.call('.','objdump','-t','-C',path)
        refs=set()
        if not f in self.libraryMap:
            refs.add(baseLibName(f))
        else:
            refs=self.libraryMap.get(f)
        dump=out.split('\n')
        for line in dump:
            parts=line.split()
            if len(parts)>=4:
                sym=parts[3]
                par=sym.find('(')
                if par>0:
                    sym=sym[0:par]
                    if not sym in symbols:
                        s=set()
                        s.update(refs)
                        symbols[sym]=s
                    else:
                        s=symbols.get(sym)
                        s.update(refs)
    
    def parseDynamic(self,path,symbols,f):
        (out,err)=utils.call('.','objdump','-T','-C',path)
        refs=set()
        if not f in self.libraryMap:
            refs.add(baseLibName(f))
        else:
            refs=self.libraryMap.get(f)
        dump=out.split('\n')
        for line in dump:
            parts=line.split()
            if len(parts)>=7:
                sym=parts[6]
                par=sym.find('(')
                if par>0:
                    sym=sym[0:par]
                if not sym in symbols:
                    s=set()
                    s.update(refs)
                    symbols[sym]=s
                else:
                    s=symbols.get(sym)
                    s.update(refs)
    
    def querySymbols(self,printout=False):
        symbols={}
        dirs=libraryDirs()
        for dir in dirs:
            try:
                files=os.listdir(dir)
                files=[f for f in files if f.endswith('.a') or f.endswith('.so')]
                for f in files:
                    path=os.path.join(dir,f)
                    if f.endswith('.a'):
                        self.parseStatic(path,symbols,f)
                    else:
                        self.parseDynamic(path,symbols,f)
            except OSError:
                pass
        if printout:
            for sym in symbols:
                print sym
                s=symbols.get(sym)
                for l in s:
                    sys.stdout.write("  "+l)
                sys.stdout.write('\n')
        return symbols
        
    def scanWorkspaceDirectory(self,dir,files=[]):
        libname=(dir.split('/'))[-1]
        self.removeLibRefs(libname)
        if len(files)==0:
            files=os.listdir(dir)
        files=[f for f in files if f.endswith('.cpp')]
        for f in files:
            path=os.path.join(dir,f)
            for line in open(path,'r').readlines():
                words=re.split('\W+',line.strip())
                for word in words:
                    if not word in self.workspaceSymbols:
                        self.workspaceSymbols[word]=set()
                    if not libname in self.workspaceLibSyms:
                        self.workspaceLibSyms[libname]=set()
                    self.workspaceSymbols.get(word).add(libname)
                    self.workspaceLibSyms.get(libname).add(word)

    def scanWorkspaceSymbols(self,printOut=False):
        self.workspaceSymbols.clear()
        self.workspaceLibSyms.clear()
        for dir,subdirs,files in os.walk(os.path.join(self.ws,'src')):
            if isLibraryDir(dir):
                self.scanWorkspaceDirectory(dir,files)
        if printOut:
            f=open('ws_syms.txt','w')
            for s in self.workspaceSymbols:
                print>>f, s
                dirs=self.workspaceSymbols.get(s)
                for d in dirs:
                    print>>f, '    '+d
            f.close()
            
    def setWorkspacePath(self,ws):
        self.ws=ws
        self.scanWorkspaceSymbols()
        
    def removeLibRefs(self,libname):
        if libname.count('/')>0:
            libname=(libname.split('/'))[-1]
        if libname in self.workspaceLibSyms:
            words=self.workspaceLibSyms.get(libname)
            for word in words:
                self.workspaceSymbols.get(word).remove(libname)
            del self.workspaceLibSyms[libname]
        


def getLibrarySymbols(ws):
    if Scanner.instance is None:
        Scanner.instance=Scanner(ws)
    return (Scanner.instance.librarySymbols,
            Scanner.instance.workspaceSymbols,
            Scanner.instance.workspaceLibSyms
           )

def setInitialResults(ws,libSyms,wsSyms,wsLibs):
    Scanner.instance=Scanner(ws,libSyms,wsSyms,wsLibs)

def rescanOnFileSave(filepath):
    dir=os.path.dirname(filepath)
    if Scanner.instance and isLibraryDir(dir):
        Scanner.instance.scanWorkspaceDirectory(dir)

def setWorkspacePath(ws):
    if Scanner.instance:
        Scanner.instance.setWorkspacePath(ws)
        return True
    return False

if __name__=='__main__':
    s=Scanner('/home/amir/workspace')
    s.queryWorkspaceSymbols(True)
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
        for line in open(os.path.join(dir,'Makefile')):
            if line.strip()=='TYPE=LIB':
                return True
    except IOError:
        pass
    return False

class Scanner:
    instance=None

    def __init__(self,ws):
        self.ws=ws
        self.packages=listAllPackages()
        self.libraryMap=self.mapLibrariesToPackages()
        self.librarySymbols=self.querySymbols()
        self.workspaceSymbols=self.queryWorkspaceSymbols()

    def mapLibrariesToPackages(self):
        libmap={}
        #f=open('pkg-libs.txt','w')
        for package in self.packages:
            #print >> f, package
            out,err=utils.call('.','pkg-config','--libs',package)
            for token in out.split():
                if token.startswith('-l'):
                    libname='lib{}'.format(token[2:])
                    #f.write("  "+libname)
                    static=libname+'.a'
                    dynamic=libname+'.so'
                    if not static in libmap:
                        libmap[static]=set()
                    libmap.get(static).add(package)                    
                    if not dynamic in libmap:
                        libmap[dynamic]=set()
                    libmap.get(dynamic).add(package)
            #f.write('\n')
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
            except OSError,e:
                pass
        if printout:
            for sym in symbols:
                print sym
                s=symbols.get(sym)
                for l in s:
                    sys.stdout.write("  "+l)
                sys.stdout.write('\n')
        return symbols

    def queryWorkspaceSymbols(self,printOut=False):
        symbols={}
        for dir,subdirs,files in os.walk(os.path.join(self.ws,'src')):
            if isLibraryDir(dir):
                libname=(dir.split('/'))[-1]
                files=[f for f in files if f.endswith('.cpp')]
                for f in files:
                    path=os.path.join(dir,f)
                    for line in open(path,'r').readlines():
                        words=re.split('\W+',line.strip())
                        for word in words:
                            if not word in symbols:
                                symbols[word]=set()
                            symbols.get(word).add(libname)
        if printOut:
            f=open('ws_syms.txt','w')
            for s in symbols:
                print>>f, s
                dirs=symbols.get(s)
                for d in dirs:
                    print>>f, '    '+d
            f.close()
        return symbols


def getLibrarySymbols(ws):
    if Scanner.instance is None:
        Scanner.instance=Scanner(ws)
    return (Scanner.instance.librarySymbols,Scanner.instance.workspaceSymbols)
    


if __name__=='__main__':
    s=Scanner('/home/amir/workspace')
    s.queryWorkspaceSymbols(True)
import sys
import os
import utils
from system import listAllPackages, libraryDirs

packages=listAllPackages()

def mapLibrariesToPackages():
    libmap={}
    #f=open('pkg-libs.txt','w')
    for package in packages:
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
    
libraryMap=mapLibrariesToPackages()


def baseLibName(f):
    if f.startswith("lib"):
        f=f[3:]
    p=f.find('.')
    if p>0:
        f=f[0:p]
    return f

def parseStatic(path,symbols,f):
    (out,err)=utils.call('.','objdump','-t','-C',path)
    refs=set()
    if not f in libraryMap:
        refs.add(baseLibName(f))
    else:
        refs=libraryMap.get(f)
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

def parseDynamic(path,symbols,f):
    (out,err)=utils.call('.','objdump','-T','-C',path)
    refs=set()
    if not f in libraryMap:
        refs.add(baseLibName(f))
    else:
        refs=libraryMap.get(f)
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

def querySymbols(printout=False):
    symbols={}
    dirs=libraryDirs()
    for dir in dirs:
        try:
            files=os.listdir(dir)
            files=[f for f in files if f.endswith('.a') or f.endswith('.so')]
            for f in files:
                path=os.path.join(dir,f)
                if f.endswith('.a'):
                    parseStatic(path,symbols,f)
                else:
                    parseDynamic(path,symbols,f)
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


librarySymbols=querySymbols()

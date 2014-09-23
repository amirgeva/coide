import sys
import os
import utils
from system import listAllPackages, libraryDirs

packages=listAllPackages()

def mapLibrariesToPackages():
    libmap={}
    for package in packages:
        out,err=utils.call('.','pkg-config','--libs',package)
        for token in out.split():
            if token.startswith('-l'):
                libname='lib{}.a'.format(token[2:])
                libmap[libname]=package
    return libmap
    
libraryMap=mapLibrariesToPackages()


def querySymbols(printout=False):
    symbols={}
    dirs=libraryDirs()
    for dir in dirs:
        try:
            files=os.listdir(dir)
            files=[f for f in files if f.endswith('.a')]
            for f in files:
                path=os.path.join(dir,f)
                (out,err)=utils.call('.','objdump','-t','-C',path)
                dump=out.split('\n')
                for line in dump:
                    parts=line.split()
                    if len(parts)>=4:
                        sym=parts[3]
                        par=sym.find('(')
                        if par>0:
                            sym=sym[0:par]
                            if f in libraryMap:
                                ref=libraryMap.get(f)
                                if not sym in symbols:
                                    s=set()
                                    s.add(ref)
                                    symbols[sym]=s
                                else:
                                    s=symbols.get(sym)
                                    s.add(ref)
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

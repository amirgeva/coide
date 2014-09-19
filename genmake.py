#!/usr/bin/env python
import os
import subprocess
import re
from properties import Properties

def listAllPackages():
    res=set()
    all=subprocess.check_output(['pkg-config','--list-all'])
    lines=all.splitlines()
    for line in lines:
        name=(line.split(' '))[0]
        res.add(name)
    return res
        
    

root=os.path.abspath('.')
print ("ROOT={}".format(root))

packages=listAllPackages()

class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    
def prt(c,s):
    print c + s + C.ENDC

def green(s):
    prt(C.GREEN,s)
    
def red(s):
    prt(C.RED,s)
    
def blue(s):
    prt(C.BLUE,s)
    
    
def isSourceDir(dir,files):
    if dir.count('/')==0:
        return False
    for f in files:
        if f.endswith('.cpp'):
            return True
    return False
    
def filterSources(files):
    alt=[]
    for f in files:
        if f.endswith('.cpp'):
            alt.append(f)
    return alt
    
def arreplace(a,fr,to):
    res=[]
    for s in a:
        res.append(s.replace(fr,to))
    return res
    
def verifyDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def generateConfig(dir,files,cfg,o):
    name=os.path.basename(dir)
    absdir=os.path.abspath(dir)
    pb=Properties(os.path.join(dir,"mk.cfg"))
    type=pb.get("TYPE")
    if len(type)==0: type="LIB"
    libs=re.split(',| ',pb.get("LIBS"))
    libs=filter(bool,libs)  # remove empty strings
    if len(type)==0:
        #red("No project type defined.")
        return False
    srcs=filterSources(files)
    intr=os.path.join(dir.replace('src/','intr/'),cfg)
    verifyDir(intr)
    outdir=os.path.join(dir.replace('src/','out/'),cfg)
    verifyDir(outdir)
    reloutdir=os.path.relpath(outdir,dir)
    globalInclude=os.path.relpath('include',dir)
    cfgInclude=''
    
    #o = open(output,'w')
    o.write('CPP_{}=g++\n'.format(cfg))
    o.write('INC_{}=-I{} {}\n'.format(cfg,globalInclude,cfgInclude))
    cflags='-c -std=c++11 $(OPT_{}) $(INC_{}) '.format(cfg,cfg)
    lflags='$(OPT_{}) $(OBJS_{}) '.format(cfg,cfg)
    for lib in libs:
        if lib in packages:
            cflags=cflags+' `pkg-config --cflags {}` '.format(lib)
            lflags=lflags+' `pkg-config --libs {}` '.format(lib)
    o.write('CFLAGS_{}={}\n'.format(cfg,cflags))
    o.write('LFLAGS_{}={}\n'.format(cfg,lflags))
    objs = arreplace(srcs,'.cpp','.o')
    for i in xrange(0,len(objs)):
        objs[i]=os.path.join(os.path.relpath(intr,dir),objs[i])
        
    o.write("OBJS_{}=".format(cfg))
    for obj in objs:
        o.write("\\\n"+obj)
    o.write("\n\n")
    o.write('{}/{}: $(OBJS_{})\n'.format(reloutdir,name,cfg))
    if type=='LIB':
        outfile='{}/lib{}.a'.format(reloutdir,name)
        o.write('\tar cr {} $(OBJS_{})\n\n'.format(outfile,cfg))
    else:
        outfile='{}/{}'.format(reloutdir,name)
        o.write('\t$(CPP_{}) -o {} $(LFLAGS_{})\n\n'.format(cfg,outfile,cfg))
        
    o.write('clean_{}:\n\trm $(OBJS_{}) {}\n\n'.format(cfg,cfg,outfile))        
    o.write('{}: {}/{}\n\n'.format(cfg,reloutdir,name))
        
    for i in xrange(0,len(objs)):
        o.write('{}: {}\n'.format(objs[i],srcs[i]))
        o.write('\t$(CPP_{}) $(CFLAGS_{}) -o {} {}/{}\n\n'.format(cfg,cfg,objs[i],absdir,srcs[i]))
    
    return True
        
def generate(dir,files):
    output=os.path.join(dir,"Makefile")
    o=open(output,"w")
    o.write('OPT_Release=-O2\n')
    o.write('OPT_Debug=-g\n')
    generateConfig(dir,files,"Release",o)
    if generateConfig(dir,files,"Debug",o):
        blue("Generated {}".format(dir))
        

def generateTree(root):
    for (dir,subdirs,files) in os.walk(root):
        if isSourceDir(dir,files):
            generate(dir,files)

def main():
    generateTree("src")

if __name__=="__main__":
    main()
    
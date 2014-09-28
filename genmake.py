#!/usr/bin/env python
import os
import re
from properties import Properties
from system import listAllPackages



root=os.path.abspath('.')
#print ("ROOT={}".format(root))

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
        
def isSourceFile(f):
    return f.endswith('.cpp')

def findMain(dir):
    pat=re.compile('(int|void)( )+main( )*\(')
    files=os.listdir(dir)
    for f in files:
        if isSourceFile(f):
            path=os.path.join(dir,f)
            lines=open(path,"r").readlines()
            for line in lines:
                if re.search(pat,line):
                    return True
    return False
            

class Generator:
    def __init__(self,root):
        self.root=root
        self.globalInc=os.path.join(root,'include')
        self.srcDir=os.path.join(root,'src')
        self.intrDir=os.path.join(root,'intr')
        self.outDir=os.path.join(root,'out')
        self.scanWorkspace()
        
    def scanWorkspace(self):
        self.wsLibs={}
        for dir,subdirs,files in os.walk(self.srcDir):
            type=""
            if isSourceDir(dir,files):
                mkPath=os.path.join(dir,'mk.cfg')
                if os.path.exists(mkPath):
                    props=Properties(mkPath)
                    if props.has("TYPE"):
                        type=props.get("TYPE")
                if type=="":
                    if findMain(dir):
                        type="APP"
                    else:
                        type="LIB"
                if type=="LIB":
                    dirname=(dir.split('/'))[-1]
                    self.wsLibs[dirname]=os.path.relpath(dir,self.srcDir)
                    

    def generateConfig(self,dir,files,cfg,o):
        name=os.path.basename(dir)
        absdir=os.path.abspath(dir)
        pb=Properties(os.path.join(dir,"mk.cfg"))
        type=pb.get("TYPE")
        if len(type)==0: 
            if findMain(absdir):
                type="APP"
            else:
                type="LIB"
        o.write('TYPE={}\n'.format(type))
        libs=re.split(',| ',pb.get("LIBS"))
        libs=filter(bool,libs)  # remove empty strings
        if len(type)==0:
            return False
        srcs=filterSources(files)
        intr=os.path.join(dir.replace(self.srcDir,self.intrDir),cfg)
        verifyDir(intr)
        outdir=os.path.join(dir.replace(self.srcDir,self.outDir),cfg)
        verifyDir(outdir)
        #reloutdir=os.path.relpath(outdir,dir)
        reloutdir=outdir
        #globalInclude=os.path.relpath(self.globalInc,dir)
        cfgInclude=''
        
        #o = open(output,'w')
        o.write('CPP_{}=g++\n'.format(cfg))
        o.write('INC_{}=-I{} {}\n'.format(cfg,self.globalInc,cfgInclude))
        cflags='-c -std=c++11 $(OPT_{}) $(INC_{}) '.format(cfg,cfg)
        lflags='$(OPT_{}) $(OBJS_{}) '.format(cfg,cfg)
        libdeps={}
        for lib in libs:
            if lib in packages:
                cflags=cflags+' `pkg-config --cflags {}` '.format(lib)
                lflags=lflags+' `pkg-config --libs {}` '.format(lib)
            else:
                if lib in self.wsLibs:
                    rel=self.wsLibs.get(lib)
                    libdir=os.path.join(self.root,'out',rel,cfg)
                    lflags=lflags+' -L{} -l{} '.format(libdir,lib)
                    libdeps[lib]=os.path.join(self.root,'src',rel)
                else:
                    lflags=lflags+' -l{} '.format(lib)
        o.write('CFLAGS_{}={}\n'.format(cfg,cflags))
        o.write('LFLAGS_{}={}\n'.format(cfg,lflags))
        objs = arreplace(srcs,'.cpp','.o')
        for i in xrange(0,len(objs)):
            #objs[i]=os.path.join(os.path.relpath(intr,dir),objs[i])
            objs[i]=os.path.join(intr,objs[i])
            
        o.write("OBJS_{}=".format(cfg))
        for obj in objs:
            o.write("\\\n"+obj)
        o.write("\n\n")
        
        liblist=[]

        for lib in libdeps:
            libname="{}_{}".format(lib,cfg)
            liblist.append(libname)
            libpath=libdeps.get(lib)
            o.write("{}:\n".format(libname))
            o.write("\t@make --no-print-directory -C {} {}\n\n".format(libpath,cfg))
        
        if type=='LIB':
            outfile='{}/lib{}.a'.format(reloutdir,name)
            o.write('{}: $(OBJS_{})\n'.format(outfile,cfg))
            o.write('\tar cr {} $(OBJS_{})\n\n'.format(outfile,cfg))
        else:
            outfile="{}/{}".format(reloutdir,name)
            o.write('OUTPUT_PATH_{}={}\n\n'.format(cfg,outfile))
            liblist=' '.join(liblist)
            o.write('{}: $(OBJS_{}) {}\n'.format(outfile,cfg,liblist))
            o.write('\t$(CPP_{}) -o {} $(LFLAGS_{})\n\n'.format(cfg,outfile,cfg))
            
        o.write('clean_{}:\n\trm $(OBJS_{}) {}\n\n'.format(cfg,cfg,outfile))        
        o.write('{}: {}\n\n'.format(cfg,outfile))
            
        for i in xrange(0,len(objs)):
            o.write('{}: {}\n'.format(objs[i],os.path.join(absdir,srcs[i])))
            o.write('\t$(CPP_{}) $(CFLAGS_{}) -o {} {}/{}\n\n'.format(cfg,cfg,objs[i],absdir,srcs[i]))
        
        return True
            
    def generate(self,dir,files):
        output=os.path.join(dir,"Makefile")
        o=open(output,"w")
        o.write('OPT_Release=-O2\n')
        o.write('OPT_Debug=-g\n')
        self.generateConfig(dir,files,"Release",o)
        if self.generateConfig(dir,files,"Debug",o):
            pass
        

def generateTree(root):
    g=Generator(root)
    for (dir,subdirs,files) in os.walk(os.path.join(root,"src")):
        if isSourceDir(dir,files):
            g.generate(dir,files)
            
def generateDirectory(root,dir):
    g=Generator(root)
    files=os.listdir(dir)
    if isSourceDir(dir,files):
        g.generate(dir,files)

def main():
    generateTree("src")

if __name__=="__main__":
    main()
    

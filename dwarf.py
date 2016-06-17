import utils
import os

class DwarfSymbols:
    def __init__(self,objpath):
        self.objpath=objpath
        self.symbols={}
        (dir,name)=os.path.split(objpath)
        (rawline,err_rawline)=utils.call(dir,'objdump','--dwarf=rawline',name)
        if err_rawline.strip().endswith('No such file'):
            raise IOError()
        self.files={}
        self.collectFiles(rawline)
        (info,err_info)=utils.call(dir,'objdump','--dwarf=info',name)
        self.collectSymbols(info)
        
    def find(self,name):
        if not name in self.symbols:
            return ('',0)
        (filenum,linenum)=self.symbols.get(name)
        return (self.files.get(filenum),linenum)
        
    def collectFiles(self,rawline):
        in_dirs=False
        in_files=False
        dirs={}
        for line in rawline.split('\n'):
            line=line.strip()
            if line.startswith('The Directory Table'):
                in_dirs=True
                continue
            if line.startswith('The File Name Table'):
                in_files=True
                continue
            if len(line)==0:
                in_dirs=False
                if in_files:
                    break
            if in_dirs:
                p=line.split()
                dirs[int(p[0])]=p[1]
            if in_files and not line.startswith('Entry'):
                p=line.split()
                if not p[-1]=='<built-in>':
                    d=int(p[1])
                    self.files[int(p[0])]=os.path.join(dirs.get(d),p[-1])
                
    def collectSymbols(self,info):
        in_sym=False
        sym_type=''
        name=''
        filenum=0
        linenum=0
        for line in info.split('\n'):
            line=line.strip()
            if (len(line)>0):
                p=line.split()
                if p[-1].startswith('(DW_TAG_'):
                    sym_type=p[-1]
                    sym_type=sym_type[8:-1]
                    in_sym=True
                    continue
                if in_sym:
                    if (p[1]=='DW_AT_name'):
                        name=p[-1]
                    if (p[1]=='DW_AT_decl_file'):
                        filenum=int(p[-1])
                    if (p[1]=='DW_AT_decl_line'):
                        linenum=int(p[-1])
                        self.symbols[name]=(filenum,linenum)
                
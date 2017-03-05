from os.path import dirname, basename, isfile
import importlib
import glob
names = glob.glob(dirname(__file__)+"/*.py")
names = [ '.'+basename(f)[:-3] for f in names if isfile(f) and basename(f)!='__init__.py']
modules=[]
for name in names:
    modules.append(importlib.import_module(name,'scm'))

def scan(root):
    for m in modules:
        res=m.scan(root)
        if res:
            return res
    return None

def diff(root,path):
    for m in modules:
        m.diff(root,path)
    
import os
import utils

def check_meld():
    res=utils.call('/','/bin/sh','-c','which meld')
    return len(res[0])>0

meld_available=check_meld()

def diff(root,path):
    if os.path.isdir(os.path.join(root,'.git')):
        if meld_available:
            utils.run(root,'meld',path)
        else:
            res=utils.call(root,'git','diff',path)
            return res[0]
    return None

def scan(root):
    if not os.path.isdir(os.path.join(root,'.git')):
        return None
    patterns={
      'Changes to be committed:':'Staged',
      'Changes not staged for commit:':'Modified',
      'Untracked files:':'Untracked'          
    }
    (out,err)=utils.call(root,'git','status','-u')
    lines=out.split('\n')
    n=len(lines)
    i=0
    status='UNKNOWN'
    scanStage=-1
    rows=[]
    while i<n:
        line=lines[i]
        for pat in patterns:
            if line.startswith(pat):
                status=patterns.get(pat)
                scanStage=0
        if len(line.strip())==0:
            if scanStage>=0:
                scanStage=scanStage+1
        elif scanStage==1:
            modifiers=[]
            filename=line.strip()
            if filename.startswith('new file:'):
                modifiers.append("New")
                filename=(filename[9:]).strip()
            if filename.startswith('modified:'):
                filename=(filename[9:]).strip()
            if filename.startswith('deleted:'):
                filename=(filename[8:]).strip()
                modifiers.append("Deleted")
            fileStatus=status
            if len(modifiers)>0:
                fileStatus=status+" ("+','.join(modifiers)+")"
            rows.append([filename,fileStatus])
        i=i+1
    return rows

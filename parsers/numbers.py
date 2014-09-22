import re

patterns=[re.compile('(\d+)$'),
          re.compile('([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')]

def parse(lines):
    res=[]
    if type(lines) is str:
        lines=lines.split('\n')
    for line in lines:
        for pat in patterns:
            m=re.match(pat,line)
            if not m is None:
                res.append((m.groups())[0])
    if len(res)>0:
        res.insert(0,'number')
    return res


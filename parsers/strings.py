import re

patterns=[re.compile('(".+")$'),
          re.compile('\{\<std::basic_string.+("[^"]*")'),
          re.compile('\{std::string = ("[^"]*")\}')]
          #re.compile('\$\d+ = ')]

def parse(lines):
    res=[]
    if type(lines) is str:
        lines=lines.split('\n')
    for line in lines:
        for pat in patterns:
            m=re.search(pat,line)
            if not m is None:
                res.append((m.groups())[0])
    if len(res)>0:
        res.insert(0,'string')
    return res



def replaces():
    return {'<std::basic_string<char, std::char_traits<char>, std::allocator<char> >>' : 'std::string'}


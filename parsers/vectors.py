import re

header=re.compile('std::vector of length (\d+), capacity (\d+) = ')
noFields=', <No data fields>'

def vectorParser(text):
    braces=0
    typepar=0
    inStr=False
    lastEsc=False
    valacc=[]
    res=[]
    n=len(text)
    skip=0
    for i in xrange(0,n):
        c=text[i]
        if skip>0:
            skip-=1
            continue
        if inStr:
            if c=='\\' and not lastEsc:
                lastEsc=True
            elif lastEsc:
                lastEsc=False
            elif c=='"':
                inStr=False
        else:
            if c=='{':
                braces+=1
            elif c=='}':
                braces-=1
            elif c=='<':
                typepar+=1
            elif c=='>':
                typepar-=1
            elif c==',' and braces==0 and typepar==0:
                if len(valacc)>0:
                    value=''.join(valacc)
                    valacc=[]
                    res.append(value)
                    skip=1
                    continue
        valacc.append(c)
    if len(valacc)>0:
        value=''.join(valacc)
        res.append(value)
    return res


def parse(lines):
    text=lines
    if type(text) is list:
        text=''.join(lines)
    text=text.replace('\n','')
    text=text.replace(noFields,'')
    m=re.match(header,text)
    res=[]
    if not m is None:
        text=re.sub(header,'',text)
        res=vectorParser(text[1:-1])
    if len(res)>0:
        res.insert(0,'vector')
    return res
        
if __name__=='__main__':
    s1='$1 = std::vector of length 3, capacity 4 = {2, 1, 7}'
    s2='$4 = std::vector of length 3, capacity 4 = {{num = 2, name = {<std::basic_string<char, std::char_traits<char>, std::allocator<char> >> = "", <No data fields>}, value = 2.2999999999999998}, {num = 2,     name = {<std::basic_string<char, std::char_traits<char>, std::allocator<char> >> = "", <No data fields>}, value = 1.8999999999999999}, {num = 7,    name = {<std::basic_string<char, std::char_traits<char>, std::allocator<char> >> = "", <No data fields>}, value = 7.4000000000000004}}'
    print parse('',s1)
    print parse('',s2)
    

import re

strPattern=re.compile("\['struct', \['std::string', '(\".*\")'\]\]")
#refPattern=re.compile()

def structParser(text):
    braces=0
    typepar=0
    inStr=False
    lastEsc=False
    keyacc=[]
    valacc=[]
    cur=keyacc
    key=''
    value=''
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
            elif c==' ' and braces==0 and typepar==0:
                if len(keyacc)>0:
                    key=''.join(keyacc)
                    keyacc=[]
                    cur=valacc
                    skip=2
                    continue
            elif c==',' and braces==0 and typepar==0:
                if len(valacc)>0:
                    value=''.join(valacc)
                    valacc=[]
                    res.append([key,value])
                    key=''
                    value=''
                    cur=keyacc
                    skip=1
                    continue
        cur.append(c)
    if len(valacc)>0:
        value=''.join(valacc)
        res.append([key,value])
    return res

def parse(lines):
    text=lines
    if type(text) is list:
        text=''.join(lines)
    text=text.replace('\n','')
    res=[]
    if text.startswith('{') and text.endswith('}'):
        res=structParser(text[1:-1])
    if len(res)>0:
        res.insert(0,'struct')
    m=re.match(strPattern,str(res))
    if not m is None:
        res=['string', (m.groups())[0]]
    return res

def replaces():
    return { ', <No data fields>' : '' }
        
if __name__=='__main__':
    s='{num = 1, name = {<std::basic_string<char, std::char_traits<char>, std::allocator<char> >> = "", <No data fields>}, value = 1}'
    print parse('',s)
    
    

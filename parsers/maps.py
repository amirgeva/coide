import re

header=re.compile('std::map with (\d+) elements = ')

def mapParser(text):
    braces=0
    brackets=0
    inStr=False
    lastEsc=False
    res=[]
    value=[]
    acckey=[]
    cur=None
    key=''
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
            if c=='"':
                inStr=True
            elif c=='{':
                braces+=1
            elif c=='}':
                braces-=1
                if braces==1 and len(key)>0:
                    valueStr=''.join(value)
                    res.append([key,valueStr])
                    value=[]
                    key=''
                    cur=None
            else:
                if c=='[':
                    brackets+=1
                    if brackets==1:
                        cur=acckey
                        continue
                elif c==']':
                    brackets-=1
                    if brackets==0 and len(acckey)>0:
                        key=''.join(acckey)
                        acckey=[]
                        value=[]
                        skip=3
                        cur=value
                        continue
        if not cur is None:
            cur.append(c)
    return res


def parse(lines):
    text=lines
    if type(text) is list:
        text=''.join(lines)
    text=text.replace('\n','')
    m=re.match(header,text)
    res=[]
    if not m is None:
        n=int((m.groups())[0])
        #print "Found map with {} elements".format(n)
        text=re.sub(header,'',text,count=1)
        res=mapParser(text)
    if len(res)>0:
        res.insert(0,'map')
    return res



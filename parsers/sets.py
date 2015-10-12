import re

header=re.compile('std::set with (\d+) elements = ')
item=re.compile('\[(\d+)\] = ([^\,\}]+)(?:\,|\})')

def setParser(text):
    items=re.findall(item,text)
    res=[]
    for i in items:
        res.append([i[0],i[1]])
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
        res=setParser(text)
    if len(res)>0:
        res.insert(0,'set')
    return res



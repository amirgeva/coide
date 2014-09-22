from PyQt4 import QtGui
import re



stringPattern=re.compile('\{std::string = (.+)$')
varPattern=re.compile('(\$\d+ = )')
#  (const Block &) @0x7fffffffdee0: 
refPattern=re.compile('\(.+&\) @0x[0-9a-f]+: ')

def flatten(val):
    if type(val) is str:
        m=re.match(stringPattern,val)
        if not m is None:
            return (m.groups())[0]
    if len(val)==0:
        return ''
    res=[str(val)]
    if type(val) is list:
        if val[0]=='struct':
            res=['{ ']
            n=len(val)
            for i in xrange(1,n):
                pair=val[i]
                if i>1:
                    res.append(", ")
                name=pair[0].strip()
                if name!='std::string':
                    res.append(name)
                    res.append('=')
                res.append(flatten(pair[1]))
            res.append(' }')
        elif val[0]=='number':
            res=[val[1]]
        elif val[0]=='string':
            res=[val[1]]
        elif val[0]=='vector':
            res=['[ ']
            n=len(val)
            for i in xrange(1,n):
                if i>1:
                    res.append(', ')
                res.append(flatten(val[i]))
            res.append(' ]')
    return ''.join(res)
        
def addSequence(item,l):
    index=0
    for sub in l:
        c=QtGui.QTreeWidgetItem([str(index)])
        c.setText(1,flatten(sub))
        item.addChild(c)
        index+=1
        
def addMapping(item,m):
    for sub in m:
        c=QtGui.QTreeWidgetItem([flatten(sub[0])])
        c.setText(1,flatten(sub[1]))
        item.addChild(c)
        
def removeVar(s):
    m=re.match(varPattern,s)
    if not m is None:
        s=re.sub(varPattern,'',s,count=1)
    return s
    
def removeRef(s):
    m=re.match(refPattern,s)
    if not m is None:
        s=re.sub(refPattern,'',s,count=1)
    return s
    

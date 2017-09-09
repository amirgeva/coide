#!/usr/bin/env python
import time
import re
import os

locframe_pat=r'<([^>]+)>'
loc_pat=r'(?:/((?:[^/]+/)*)([^/]+):(\d+):(\d+), )?line:(\d+):(\d+)(?:, col:(\d+))?'

class Location:
    def __init__(self,l):
        self.dir=l[0]
        if self.dir:
            self.dir=os.path.abspath(self.dir)
        self.filename=l[1]
        self.line=None
        if l[4]:
            self.line=int(l[4])
        self.col=None
        if l[6]:
            self.col=int(l[6])
            
    def __str__(self):
        res=''
        if self.dir:
            res=os.path.join(self.dir,self.filename)+':'
        if self.line:
            res=res+str(self.line)
        else:
            res=res+'-'
        if self.col:
            res=res+':'+str(self.col)
        return res

class Node:
    def __init__(self,s):
        self.text=s.strip()
        self.children=[]
        self.loc=None
        if self.text:
            p=self.text.split()
            self.node_type=p[0]
            m=re.search(locframe_pat,self.text)
            if m:
                loc_text=m.groups()[0]
                m=re.match(loc_pat,loc_text)
                if m:
                    loc=m.groups()
                    self.loc=Location(loc)
                    #print self.loc
        
    def add_child(self,s):
        child=Node(s)
        self.children.append(child)
        return child
        
    def tostr(self,indent=0):
        res=' '*indent+self.text+'\n'
        for c in self.children:
            res=res+c.tostr(indent+2)
        return res

def load_tree(f):
    lastj=0
    root=Node('')
    stack=[root]
    last_node=None
    line_index=0
    try:
        for line in f:
            j=0
            line_index=line_index+1
            for i in xrange(0,len(line)):
                if line[i].isalpha() or line[i]=='<':
                    j=i
                    break
            if j > lastj:
                stack.append(last_node)
            while j < lastj:
                del stack[-1]
                lastj=lastj-2
            last_node=stack[-1].add_child(line[j:])
            lastj=j
            if (lastj/2 + 1)!=len(stack):
                print "Mismatch at line: {}".format(line_index)
                break
    except IndexError:
        print "IndexError at line: {}".format(line_index)
    return root
            
            
if __name__=='__main__':
    t0=time.time()
    root=load_tree(open('f200','r'))
    print time.time()-t0
    #print root.tostr()
    
#!/usr/bin/env python
import sys
from xlex import Lexer
from xnode import Node

dev=False

class ParseException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)


def recursive_find(seq,start,stop,innermost=False):
    laststart=-1
    for i in xrange(0,len(seq)):
        if seq[i]==start:
            laststart=i
            depth=1
            for j in xrange(i+1,len(seq)):
                if seq[j]==start: 
                    laststart=j
                    depth+=1
                if seq[j]==stop:
                    depth-=1
                    if innermost:
                        return (laststart,j+1)
                if depth==0:
                    return (i,j+1)
    return None

def recursive_unite(seq,start,stop,name):
    while True:
        idx=recursive_find(seq,start,stop)
        if not idx:
            break
        i=idx[0]
        seq[i].name=name
        for j in xrange(i+1,idx[1]):
            seq[i].value+=seq[i+1].value
            del seq[i+1]

def unite_ident(seq):
    n=len(seq)
    i=0
    while i<n:
        if seq[i]=='IDENT':
            while (i+1)<n and seq[i+1]!='EQUALS':
                if seq[i+1]!='COMMA':
                    seq[i].value+=' '
                seq[i].value+=seq[i+1].value
                del seq[i+1]
                n-=1
        i+=1
                    
def match(seq,sub,i):
    if (i+len(sub))>len(seq):
        return False
    for j in xrange(0,len(sub)):
        if not sub[j]:
            continue
        if seq[i+j]!=sub[j]:
            return False
    return True
            
                    
def collapse(seq,sub):
    n=len(seq)
    m=len(sub)
    i=0
    while i<n:
        if match(seq,sub,i):
            for j in xrange(0,m):
                if sub[m-j-1]:
                    del seq[i+m-j-1]
                    n-=1
        else:
            i+=1

def collapse_all(seq):
    recursive_unite(seq,'LTAG','RTAG','TAG')
    collapse(seq,['TAG','EQUALS'])
    collapse(seq,['COMMA','TAG'])
    unite_ident(seq)
    n=len(seq)
    while True:
        collapse(seq,['LBRACE','','RBRACE'])
        collapse(seq,['LBRACKET','','RBRACKET'])
        m=len(seq)
        if m==n:
            break
        n=m
    recursive_unite(seq,'LBRACKET','RBRACKET','INDEX')
        
        
def split_seq(seq,delim):
    res=[]
    cur=[]
    for t in seq:
        if t==delim:
            if len(cur)>0:
                res.append(cur)
                cur=[]
        else:
            cur.append(t)
    if len(cur)>0:
        res.append(cur)
    return res

ignore_list=['_vptr','static ']

def value_node(seq):
    if len(seq)==1:
        return seq[0]
    if len(seq)==5 and seq[1]=='EQUALS' and seq[3]=='EQUALS':
        res=seq[4]
        res.name=seq[0].value
        res.value=seq[2].value
        return res
    if seq[1]=='EQUALS':
        if seq[2]=='TAG':
            return None
        for ig in ignore_list:
            if seq[0].value.startswith(ig):
                return None
        res=seq[2]
        res.name=seq[0].value
        return res
    return None

def dump(seq,indent=0):
    res=''
    s=' '*indent
    for node in seq:
        res+='{}{}={}\n'.format(s,node.name,node.value)
        res+=dump(node.children,indent+2)
    return res

        
class Parser(object):
    def __init__(self,text):
        seq=[Node(t.token,t.value) for t in Lexer(text).all()]
        collapse_all(seq)
        self.root=self.parse(seq)

    def finalize_root(self,seq):
        if len(seq)==5 and seq[1]=='EQUALS' and seq[3]=='EQUALS':
            root=seq[4]
            root.name=seq[0].value
            root.value=seq[2].value
            return root
        if len(seq)==3 and seq[1]=='EQUALS':
            root=seq[2]
            root.name=seq[0].value
            return root
        return None

    def parse(self,seq):
        while True:
            idx=recursive_find(seq,'LBRACE','RBRACE',True)
            if not idx:
                return self.finalize_root(seq)
            sub=seq[(idx[0]+1):(idx[1]-1)]
            sibs=split_seq(sub,'COMMA')
            cur=Node('UNDEF','struct')
            cur.children=[value_node(s) for s in sibs]
            cur.children=[c for c in cur.children if c]
            seq[idx[0]]=cur
            del seq[(idx[0]+1):idx[1]]
            if dev: print "{}\n\n".format(dump(seq))


def test():
    global dev
    dev=True
    for i in xrange(1,len(sys.argv)):
        arg=sys.argv[i]
        print arg
        text=open(arg,'r').read()
        print text
        p=Parser(text)
        print dump([p.root])

if __name__=='__main__':
    test()
    

#!/usr/bin/env python
import sys
from xlex import Lexer
from xnode import Node

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
        seq[i].token=name
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

def print_seq(seq):
    indent=0
    for t in seq:
        if t.token=='RBRACE': indent-=2
        print '{}{} : {}'.format(' '*indent,t.token,t.value)
        if t.token=='LBRACE': indent+=2

def value_node(seq):
    print seq
    res=Node(seq[0].value)
    if seq[1].token=='EQUALS':
        res.value=seq[2].value
    return res
        
class Parser(object):
    def __init__(self,text):
        seq=[t for t in Lexer(text).all()]
        collapse_all(seq)
        self.root=self.parse(seq)
        print_seq(seq)
        
    def parse(self,seq):
        while True:
            idx=recursive_find(seq,'LBRACE','RBRACE',True)
            if not idx:
                break
            sub=seq[(idx[0]+1):(idx[1]-1)]
            sibs=split_seq(sub,'COMMA')
            cur=Node()
            cur.children=[value_node(s) for s in sibs]
            seq[idx[0]].token='NODE'
            seq[idx[0]].value=cur
            del seq[(idx[0]+1):idx[1]]
                

def test():
    for i in xrange(1,len(sys.argv)):
        arg=sys.argv[i]
        print arg
        text=open(arg,'r').read()
        print text
        p=Parser(text)

if __name__=='__main__':
    test()
    

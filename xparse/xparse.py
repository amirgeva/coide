#!/usr/bin/env python
from xlex import Lexer
from xnode import Node
#import re

#stdpat=re.compile('{<.+>=(.+)(,.+)}')
#
#def parse_name(s):
#    m=re.match(stdpat,s)
#    if m:
#        g=m.groups()
#        return g[0]
#    return s
    

class ParseException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

class Parser:
    def __init__(self,text):
        #print "Parsing: '{}'".format(text)
        self.lexer=Lexer(text)
        self.root=Node(self.expect('IDENT'))
        self.expect('EQUALS')
        self.parse(self.root,'')
        
    def expect(self,token):
        t,v=self.lexer.analyze()
        if t!=token:
            rest=self.lexer.get_rest()
            raise ParseException("Syntax error.  Expected {}, got {}\n{}".format(token,t,rest))
        return v
        
    def readUntil(self,token):
        res=''
        while True:
            t,v=self.lexer.analyze(True)
            if t==token:
                break
            res=res+v
        return res
        
    def parseName(self,tagdepth):
        name=''
        try:
            while True:
                t,v=self.lexer.analyze(True)
                if t=='LTAG':
                    tagdepth=tagdepth+1
                if t=='RTAG':
                    tagdepth=tagdepth-1
                if tagdepth<1:
                    break
                name=name+v
        except EndOfText:
            t="END"
        return name
        
    def parse(self,node,initvalue):
        value=initvalue
        tagdepth=0
        try:
            while True:
                t,v=self.lexer.analyze()
                if t=='LTAG':
                    tagdepth=tagdepth+1
                if t=='RTAG':
                    tagdepth=tagdepth-1
                if tagdepth==0:
                    #if not t or t=='COMMA' or t=='RBRACE':
                    if not t or t=='RBRACE':
                        break
                    if t=='LBRACE':
                        value='struct'
                        self.lexer.push()
                        self.parse_children(node)
                        break
                    if t=='EQUALS':
                        self.parse_children(node)
                        break
                if len(value)>0:
                    value=value+' '
                value=value+v
                node.value=value
        except EndOfText:
            t="END"
        node.value=value
        if node.value=='struct' and len(node.children)==1 and node.children[0].name.startswith('std::') and node.children[0].value:
            node.value=node.children[0].value
            node.children=[]
        return (value,t)
        
    def parse_children(self,node):
        self.expect('LBRACE')
        count=0
        while True:
            (t,v)=self.lexer.analyze()
            if t=='COMMA':
                continue
            if t=='RBRACE':
                break
            if t=='LBRACE':
                self.lexer.push()
                child=Node(str(count))
                count=count+1
                node.add_child(child)
                self.parse_children(child)
                continue
            elif t=='LBRACKET':
                parts=[]
                while t!='RBRACKET':
                    t,name=self.lexer.analyze()
                    if t!='RBRACKET':
                        parts.append(name)
                #self.expect('RBRACKET')
                self.expect('EQUALS')
                child=Node(''.join(parts))
                v=''
            elif t=='LTAG': 
                # base class
                name=self.parseName(1)
                if name=='No data fields':
                    continue
                child=Node(name)
                self.expect('EQUALS')
                v=''
            elif t=='IDENT':
                v=v+self.readUntil('EQUALS')
                child=Node(v)
                v=''
            else:
                child=Node(str(count))
                count=count+1
            node.add_child(child)
            (cv,t)=self.parse(child,v)
            if t=='RBRACE':
                break
        if not node.value and len(node.children)>0:
            for c in node.children:
                if node.value:
                    node.value=node.value+", "
                if c.value:
                    node.value=node.value+c.value
                else:
                    node.value=node.value+'{}'
            

def test():
    import sys
    for i in xrange(1,len(sys.argv)):
        arg=sys.argv[i]
        print arg
        text=open(arg,'r').read()
        print text
        p=Parser(text)
        print p.root

if __name__=='__main__':
    test()
    

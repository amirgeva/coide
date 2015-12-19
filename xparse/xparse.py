#!/usr/bin/env python
from xlex import Lexer,TokenizerException,EndOfText

class Node:
    def __init__(self,name='',value=''):
        self.name=name
        self.value=value
        self.children=[]
        
    def add_child(self,c):
        self.children.append(c)
        
    def iprint(self,indent):
        res=' '*indent+self.name+"="+self.value
        if len(self.children)>0:
            res=res+" {\n"
            for c in self.children:
                res=res+c.iprint(indent+2)
            res=res+' '*indent+"}\n"
        else:
            res=res+'\n'
        return res
        
    def __repr__(self):
        return self.iprint(0)

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
        
    def parse(self,node,initvalue):
        value=initvalue
        try:
            while True:
                t,v=self.lexer.analyze()
                if not t or t=='COMMA' or t=='RBRACE':
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
        except EndOfText,e:
            t="END"
        node.value=value
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
            if t=='LBRACKET':
                t,name=self.lexer.analyze()
                self.expect('RBRACKET')
                self.expect('EQUALS')
                child=Node(name)
                v=''
            elif t=='IDENT':
                self.expect('EQUALS')
                child=Node(v)
                v=''
            else:
                child=Node(str(count))
                count=count+1
            node.add_child(child)
            (cv,t)=self.parse(child,v)
            if t=='RBRACE':
                break

def test():
    import sys
    for i in xrange(1,len(sys.argv)):
        arg=sys.argv[i]
        print arg
        text=open(arg,'r').read()
        print text
        indent=0
        p=Parser(text)
        print p.root

if __name__=='__main__':
    test()
    

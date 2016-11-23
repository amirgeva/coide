#!/usr/bin/env python

class Node:
    def __init__(self,name='',value=''):
        self.name=name
        self.value=value
        self.children=[]
        
    def add_child(self,c):
        self.children.append(c)
        
    def iprint(self):
        res=self.name+"="+str(self.value)
        if len(self.children)>0:
            res=res+"{"
            for c in self.children:
                try:
                    res=res+' '+str(c)
                except TypeError:
                    print "ERR:"
                    print type(c)
                    print c
            res=res+" }"
        return res
        
    def __str__(self):
        return self.iprint()
        #return '{}={}'.format(self.name,self.value)
        
    def __repr__(self):
        return self.iprint()



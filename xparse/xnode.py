#!/usr/bin/env python

class Node:
    def __init__(self,name='',value=''):
        self.name=name
        self.value=value
        self.children=[]
        
    def add_child(self,c):
        self.children.append(c)
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return "N({}:{})".format(self.name,self.value)

    def __eq__(self,other):
        return self.name==str(other)

    def __ne__(self, other):
        return self.name != str(other)

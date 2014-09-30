import os
import re

class Properties:
    def __init__(self,path=''):
        self.props={}
        if path and os.path.exists(path):
            lines=open(path).readlines()
            for line in lines:
                parts=line.strip().split('=')
                if len(parts)==2:
                    self.props[parts[0]]=parts[1]
    
    def copyFrom(self,props):
        self.props=props.props.copy()
    
    def has(self,name):
        return name in self.props

    def get(self,name,default=''):
        if name in self.props:
            return self.props.get(name)
        return default
        
    def assign(self,name,value):
        self.props[name]=value
        
    def search(self,exp):
        '''
        Returns a list of name that match the regular expression
        '''
        res=[]
        for name in self.props:
            if re.match(exp,name):
                res.append(name)
        return res

    def save(self,path):
        f=open(path,"w")
        if f:
            for p in self.props.keys():
                f.write('{}={}\n'.format(p,self.get(p)))
            f.close()

import os
import re

class Properties:
    def __init__(self,path=''):
        self.props={}
        if path and os.path.exists(path):
            lines=open(path).readlines()
            for line in lines:
                line=line.strip()
                p=line.find('=')
                if p>0:
                    name=line[0:p]
                    value=line[p+1:]
                    self.props[name]=value
    
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
        
    def remove(self,name):
        if name in self.props:
            del self.props[name]

    def keys(self):
        return self.props.keys()

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

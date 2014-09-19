import os

class Properties:
    def __init__(self,path=''):
        self.props={}
        if os.path.exists(path):
            lines=open(path).readlines()
            for line in lines:
                parts=line.strip().split('=')
                if len(parts)==2:
                    self.props[parts[0]]=parts[1]

    def get(self,name):
        if name in self.props:
            return self.props.get(name)
        return ''
        
    def assign(self,name,value):
        self.props[name]=value

    def save(self,path):
        f=open(path,"w")
        if f:
            for p in self.props.keys():
                f.write('{}={}\n'.format(p,self.get(p)))
            f.close()

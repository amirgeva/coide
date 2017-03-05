import re

varPattern=re.compile('(\$\{[^\}]+\})')
mkvarPattern=re.compile('(\$\([^\)]+\))')

def replaceMacros(pat,code,props):
    while True:
        m=re.search(pat,code)
        if m is None:
            break
        s=(m.groups())[0]
        var=s[2:-1]
        value=props.get(var)
        code=code.replace(s,value)
    return code


def generateCode(code,props):
    return replaceMacros(varPattern,code,props)
    
def generateMkCommand(code,props):
    return replaceMacros(mkvarPattern,code,props)
import re

varPattern=re.compile('(\$\{[^\}]+\})')

def generateCode(code,props):
    while True:
        m=re.search(varPattern,code)
        if m is None:
            break
        s=(m.groups())[0]
        var=s[2:-1]
        value=props.get(var)
        code=code.replace(s,value)
    return code



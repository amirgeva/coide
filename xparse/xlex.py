#!/usr/bin/env python
import re

token_pattern = r"""
(?P<IDENT>[a-zA-Z_\$][a-zA-Z0-9_:]*)
|(?P<HEX>0x[0-9a-fA-F]+)
|(?P<FLOAT>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)
|(?P<INTEGER>[0-9]+)
|(?P<DOT>\.)
|(?P<AST>\*)
|(?P<STRING>\"[^\"]*\")
|(?P<COLON>\:)
|(?P<COMMA>\,)
|(?P<VAR>\$\d+)
|(?P<LBRACE>[{])
|(?P<RBRACE>[}])
|(?P<LBRACKET>\[)
|(?P<RBRACKET>\])
|(?P<LPAREN>[()])
|(?P<RPAREN>[)])
|(?P<LTAG>[<)])
|(?P<RTAG>[>])
|(?P<NEWLINE>\n)
|(?P<WS>\s+)
|(?P<EQUALS>[=])
|(?P<SLASH>[/])
"""

token_re = re.compile(token_pattern, re.VERBOSE)

class TokenizerException(Exception): pass
class EndOfText(Exception): pass

def parse_string(text):
    cur=1
    esc=False
    while cur<len(text):
        c=text[cur]
        if c=='\\':
            esc=not esc
        else:
            if c=='"' and not esc:
                break
            esc=False
        cur=cur+1
    return text[0:(cur+1)]
    
class Lexer:
    def __init__(self,text):
        self.text=text
        self.pos=0
        self.lastToken=''
        self.lastValue=''
        self.queue=[]
        
    def get_rest(self):
        return self.text[self.pos:]
        
    def analyze(self):
        if len(self.queue)>0:
            tokname,tokvalue = self.queue[0]
            del self.queue[0]
        else:
            if self.pos>=len(self.text):
                raise EndOfText()
            if self.text[self.pos]=='"':
                tokname='STRING'
                tokvalue = parse_string(self.text[self.pos:])
                self.pos=self.pos+len(tokvalue)
            else:
                m = token_re.match(self.text, self.pos)
                if not m:
                    raise TokenizerException('tokenizer stopped at pos %r of %r' % (self.pos, len(self.text)))
                self.pos = m.end()
                tokname = m.lastgroup
                tokvalue = m.group(tokname)
                if tokname=='WS' or tokname=='NEWLINE':
                    return self.analyze()
        self.lastToken=tokname
        self.lastValue=tokvalue
        return (tokname,tokvalue)

    def push(self):
        self.queue.insert(0,(self.lastToken,self.lastValue))

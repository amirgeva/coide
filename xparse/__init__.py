#!/usr/bin/env python
from xparse import Parser
from xlex import TokenizerException,EndOfText

def parse(text):
    #print "Parsing: '{}'".format(text)
    try:
        return Parser(text).root
    except TokenizerException,e:
        pass
    except EndOfText,e:
        pass



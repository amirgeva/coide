#!/usr/bin/env python
from xparse2 import Parser, ParseException
from xlex import TokenizerException,EndOfText

def parse(text):
    if text=='No locals.':
        return None
    try:
        if text.find('error reading variable:')>=0:
            return None
        p=Parser(text)
        p.flatten()
        return p.root
    except TokenizerException:
        pass
    except EndOfText:
        pass
    except ParseException:
        print "Failed to parse '{}'".format(text)



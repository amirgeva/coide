#!/usr/bin/env python
from xparse import Parser, ParseException
from xlex import TokenizerException,EndOfText

def parse(text):
    if text=='No locals.':
        return None
    try:
        if text.find('error reading variable:')>=0:
            return None
        return Parser(text).root
    except TokenizerException,e:
        pass
    except EndOfText,e:
        pass
    except ParseException,e:
        print "Failed to parse '{}'".format(text)



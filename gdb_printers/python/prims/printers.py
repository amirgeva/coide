import gdb
import re

pointer = re.compile(r"[_A-Za-z]\w* \*\Z")

class PointerPrinter(object):
    def __init__(self,val):
        v=val.cast(gdb.lookup_type('unsigned'))
        v=int(str(v))
        self.val=str(hex(v))
        self.type=str(val.type)
    
    def to_string(self):
        return "({}) {}".format(self.type,self.val)

def prim_printer_lookup(val):
    t=str(val.type)
    if t=='char *' or t=='const char*':
        return None
    if pointer.match(t):
        return PointerPrinter(val)
    return None

def register_prim_printers():
    gdb.pretty_printers.append(prim_printer_lookup)


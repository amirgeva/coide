

mw=None
dev=False

# It's important to have .cpp before .c  for replace function when creating .o names
src_exts=['.cpp','.c']
hdr_exts=['.hpp','.h']

def is_src_ext(path):
    for e in src_exts:
        if path.endswith(e):
            return True
    return False
    
def is_header(path):
    for e in hdr_exts:
        if path.endswith(e):
            return True
    return False
    
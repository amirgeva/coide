# Settings are always a tuple, where the first two members 
# are 'name' and 'title'
# The third member can be either:
#   1.  a string containing pipe delimited pulldown options
#       if an option has parentheses, its contents are the actual flag to be used
#   2.  'CB' for a checkbox, followed by a boolean member for the default, 
#       and the flag that is used if true
#   3.  'STR' for a single-line string value, followed by the string default
#   4.  'EDIT' for a multi-line string value, followed by the string default

tabs={
    'Compile':[
        ('OPT_Release','Optimization','-O0|-O1|-O2|-O3','-O2'),
        ('COMPILE_PIC','Position Independent Compilation','CB',True,'-fPIC'),
        ('COMPILE_WARN','Warnings','Default|None (-w)|All (-Wall)','Default'),
        ('COMPILE_PEDANTIC','Pedantic','CB',False,'-pedantic-errors'),
        ('COMPILE_WARNERR','Warning as errors','CB',False,'-Werror'),
        ('COMPILE_FATAL_ERROR','Stop after first error','CB',False,'-Wfatal-errors'),
        ('COMPILE_CPP_STD','Standard','Default|-std=c++0x|-std=c++11|-std=c++14|-std=c++17','-std=c++11'),
        ('COMPILE_SIMD','SIMD Flag','Default|-mavx','Default')
    ],
    'Link':[
        ('LINK_PTHREAD','pthread','Default|On (-pthread)','Default')
    ],
    'Advanced':[
        ('COMPILER','Compiler','STR','g++'),
        ('COMPILE_CUSTOM','Custom Compile Flags','EDIT',''),
        ('LINK_CUSTOM','Custom Link Flags','EDIT',''),
        ('BUILD_WHOLE_ARCHIVE','Whole Archive','CB',False,'')
    ]
}


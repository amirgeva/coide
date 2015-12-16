# Settings are always a tuple, where the first two members 
# are 'name' and 'title'
# The third member can be either:
#   1.  a string containing pipe delimited pulldown options
#   2.  'CB' for a checkbox, followed by a boolean member for the default
#   3.  'STR' for a string value, followed by the string default

tabs={
    'Compile':[
        ('BUILD_OPT','Optimization','-O0|-O1|-O2|-O3','-O2'),
        ('BUILD_WARN','Warnings','Default|None (-w)|All (-Wall)','Default'),
        ('BUILD_PEDANTIC','Pedantic','CB',False),
        ('BUILD_WARNERR','Warning as errors','CB',False),
        ('BUILD_CPP11','C++11','CB',True)
    ],
    'Link':[
    ],
    'Advanced':[
        ('BUILD_CUSTOM_COMPILE','Custom Compile Flags','EDIT',''),
        ('BUILD_CUSTOM_LINK','Custom Link Flags','EDIT','')
    ]
}


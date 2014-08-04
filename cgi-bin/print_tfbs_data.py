#!/usr/bin/env python

import cgi
import yate
from TFBS_tools import print_tfbs

def split_input(field):
    a=[]
    b=[]
    for i in field.split(','):
        a.append(i.strip())
    for i in a:
        for c in i.split():
            b.append(c.strip())
    return b    

form_data = cgi.FieldStorage().getvalue('id')
print(yate.start_response())
print(yate.include_header(''))  
print_tfbs([form_data])
print(yate.include_footer(""))

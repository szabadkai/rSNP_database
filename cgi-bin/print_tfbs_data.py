#!/usr/bin/env python

import cgi
from mysql_open import *
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
TFBS_tools.print_tfbs(form_data)
print(yate.include_footer({""}))




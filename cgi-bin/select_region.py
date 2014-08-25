#!/usr/bin/env python
from TFBS_tools import print_tfbs
from TFBS_tools import return_intervall

import cgi
import yate

form_data = cgi.FieldStorage()
c = form_data.getvalue('chr')
s = form_data.getvalue('start')
t = form_data.getvalue('stop')


print(yate.start_response())
print(yate.include_header(''))  
print_tfbs(return_intervall(c,s, t))
print(yate.include_footer(""))

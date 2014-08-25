#!/usr/bin/env python
from TFBS_tools import print_tfbs
from TFBS_tools import return_intervall

import cgi
import yate

form_data = cgi.FieldStorage()
Chr=form_data['chr']
Start=form_data['start']
Stop=form_data['stop']

print(yate.start_response())
print(yate.include_header(''))  
print_tfbs(return_intervall(Chr,Start,Stop))
print(yate.include_footer(""))

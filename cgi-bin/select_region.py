#!/usr/bin/env python
from TFBS_tools import print_tfbs
from TFBS_tools import return_intervall
import MySQLdb as mdb

import cgi
import yate

Chr = cgi.FieldStorage().getvalue('chr')
Start = cgi.FieldStorage().getvalue('start')
Stop = cgi.FieldStorage().getvalue('stop')

print(yate.start_response())
print(yate.include_header(''))  
print_tfbs(return_intervall(Chr,Start,Stop))
print(yate.include_footer(""))

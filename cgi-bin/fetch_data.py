#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import cgi
import cgitb
import yate
cgitb.enable()

form_data = cgi.FieldStorage()

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

print(yate.start_response())
print(yate.include_header("the folloving stuff was requested:"))    
print(yate.header("STUFF"))

with con: 

    cur = con.cursor()
    cur.execute("SELECT matrix_bin FROM matrix LIMIT 1")

    rows = cur.fetchall()
    
    print('<p class="preserve">')
    for d in rows:
        d=d[0].replace('\n','<br>')
        print(d)
    print('</p>')

print(yate.include_footer({"Home": "/index.html"}))
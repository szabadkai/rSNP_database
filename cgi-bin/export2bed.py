#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['chr','start','stop','peak']

form_data = cgi.FieldStorage().getvalue('exp')



print(yate.start_response())

with con: 
    print '<table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS 
                    WHERE TFBS.experiment='%s' order by chr ;""" % form_data)
    rows = cur.fetchall()

    for row in rows:
        for col in header_order:
            print "%s<br>" % row[col]
    else:
        pass
print(yate.include_footer({""}))

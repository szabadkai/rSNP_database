#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('exp')



print(yate.start_response())

with con: 
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS 
                    WHERE TFBS.experiment='%s' order by chr ;""" % form_data)
    rows = cur.fetchall()

    for row in rows:
        print "%s\t%s\t%s" % (row['chr'],row['peak_start'],row['peak_stop'])
    else:
        pass
print(yate.include_footer({""}))

#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('id')

print(yate.start_response())
print(yate.include_header(""))  
print "rSNP: "+form_data
with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT RS.*,MATRIX.*,TFBS.*
                    FROM RS,MATRIX,TFBS
                    WHERE RS.rs_ID = %r AND
                    TFBS.TFBS_ID=RS.TFBS_ID AND
                    TFBS.matrix_id = MATRIX.matrix_id;""" % form_data)
    rows = cur.fetchall()
    a=rows[0]['matrix_bin'].split()
    print a

print(yate.include_footer())
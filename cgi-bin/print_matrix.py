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
    a=rows[0]['matrix_bin'].split('\n')

    print '<div class="input_field"><table><thead>'
	# for col in ['A','T','G','C']:
	# 	print "<th>%s</th>" % col
	# print "</thead>"
	# for row in a:
	#     print "<tr>"
	#     for i in row.split():
	#     	print "<th>%s</th>" % i
	#     print "</tr>"
	# print("</table></div>")

print(yate.include_footer())
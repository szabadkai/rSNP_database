#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('id')
pos = cgi.FieldStorage().getvalue('pos')
minor = cgi.FieldStorage().getvalue('minor')
major = cgi.FieldStorage().getvalue('major')
print(yate.start_response())
print(yate.include_header(""))  
print "rSNP: "+form_data
ind={'A':0,'C':1,'G':2,'T':3}

with con:
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute(""" SELECT RS.*,MATRIX.*,TFBS.*
				FROM RS,MATRIX,TFBS
				WHERE RS.rs_ID = %r AND
				TFBS.TFBS_ID=RS.TFBS_ID AND
				TFBS.matrix_id = MATRIX.matrix_id;""" % form_data)
	rows = cur.fetchall()
	a=rows[0]['matrix_bin'].split('\n')
	print pos+"\t"+minor+"\t"+major
	print '<table><tr>'
	for col in ['Position','A','C','G','T']:
		print "<th>%s</th>" % col
	print "</tr>"
	count=1

	for row in a[1:-1]:
		if int(pos)==count:
			print "<tr>"
			print "<td>%s</td>" % count
			count = count +1
			for i,j  in enumerate(row.split()):
				if i == ind[minor]:
					print "<td style='background-color:yellow;'>%s</td>" % j 
				elif i == ind[major]:
					print "<td style='background-color:red;'>%s</td>" % j 
				else:
					print "<td>%s</td>" % j
			print "</tr>"
		else:
			print "<tr>"
			print "<td>%s</td>" % count
			count = count +1
			for i in row.split():
				print "<td>%s</td>" % i
			print "</tr>"
	print("</table>")

	print(yate.include_footer(""))
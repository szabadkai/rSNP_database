#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

form_data = cgi.FieldStorage()['SNPs'].value


print(yate.start_response())
print(yate.include_header("DATA"))  
print(yate.para('fetching:\t'+form_data))
with con: 
    print('<table><thead><tr><th>rSNP</th><th>TFBS</th></tr></thead><tr>')
    cur = con.cursor()
    cur.execute("SELECT RS.RS_ID,TFBS.TFBS_ID FROM TFBS,RS where RS.RS_ID=%r and TFBS.TFBS_ID=RS.TFBS_ID" % form_data)
    rows = cur.fetchall()
    print "<th><a href='print_rsnp_data.py?id=%s'>%s</th>" % (str(rows[0][0]),str(rows[0][0]))
    print "<th><a href='print_tfbs_data.py?id=%s'>%s</th>" % (str(rows[0][1]),str(rows[0][1]))

print("</tr></table>")       
print(yate.include_footer({"Home": "/index.html"}))

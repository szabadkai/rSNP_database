#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

form_data = cgi.FieldStorage().getvalue('id')



print(yate.start_response())
print(yate.include_header("DATA"))  
with con: 
    print('<table>')
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM TFBS,ORTHOLOGS where TFBS_ID='%s' AND TFBS.peak = ORTHOLOGS.peak" % form_data)
    rows = cur.fetchall()
    ort = {'peak':rows[0]['peak'],'data':rows[0]['data']}
    del rows[0]['data']
    yate.table(rows)
    print("</table><br>")
    print('<table>')
    yate.table([ort])
    print("</table><br>")
    print("<a href='ortho_fasta.py?peak=%s'>download fasta</a>" % rows[0]['peak'])
print(yate.include_footer({"Home": "/index.html"}))

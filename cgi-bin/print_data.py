#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import cgitb
cgitb.enable()
import yate

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

form_data = cgi.FieldStorage()['SNPs'].value

print(yate.start_response())
print(yate.include_header("DATA"))  
print(yate.para('fetching'+form_data))
with con: 
    print('<div class="CSSTableGenerator" ><table><tr>')
    cur = con.cursor()
    cur.execute("SELECT RS.RS_ID,TFBS.TFBS_ID,TFBS.seq,RS.major_al,RS.freq_major,RS.minor_al,RS.freq_min FROM TFBS,RS where RS.RS_ID=%r and TFBS.TFBS_ID=RS.TFBS_ID" % form_data)

    rows = cur.fetchall()
    for i in rows[0]:
        print("<th>"+str(i)+"</th>")
        
        
print("</tr></table></div>")       
print(yate.include_footer({"Home": "/index.html"}))
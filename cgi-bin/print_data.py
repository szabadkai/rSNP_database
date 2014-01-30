#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

def split_input(field):
    a=[]
    b=[]
    for i in field.split(','):
        a.append(i.strip())
    for i in a:
        for c in i.split():
            b.append(c.strip())
    return b        
           
con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  

field = cgi.FieldStorage()['SNPs'].value

with con: 
    print '<div class="input_field"><table><thead><tr><th>rSNP</th><th>TFBS</th></tr></thead>'
    for form_data in split_input(field):
        try:
            cur = con.cursor()
            cur.execute(""" SELECT RS.RS_ID,TFBS.TFBS_ID 
                            FROM TFBS,RS 
                            WHERE RS.RS_ID=%r AND 
                            TFBS.TFBS_ID=RS.TFBS_ID""" % form_data)
            rows = cur.fetchall()
            print "<tr><th><a href='print_rsnp_data.py?id=%s'>%s</a></th>" % (str(rows[0][0]),str(rows[0][0]))
            print "<th><a href='print_tfbs_data.py?id=%s'>%s</a></th>" % (str(rows[0][1]),str(rows[0][1]))
            print "</tr>"
        except:
            pass
print("</table></div><br>")       
print(yate.include_footer({""}))

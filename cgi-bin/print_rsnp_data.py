#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

form_data = cgi.FieldStorage().getvalue('id')



print(yate.start_response())
print(yate.include_header("DATA"))  
with con:
    print "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>NCBI-dbSNP</a><br>" % form_data.split('_')[0][2:]
    print('<table>')
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT RS.*, MATRIX.matrix_bin FROM TFBS,MATRIX,RS where RS_ID='%s' AND TFBS.TFBS_ID=RS.TFBS_ID and TFBS.matrix_id=MATRIX.matrix_ID" % form_data)
    rows = cur.fetchall()
    matrix = rows[0]['matrix_bin']
    del rows[0]['matrix_bin']
    yate.table(rows)
    print("</tr></table>")   
    print(yate.para(matrix.replace('\n','<br>')))
    
print(yate.include_footer({"Home": "/index.html"}))

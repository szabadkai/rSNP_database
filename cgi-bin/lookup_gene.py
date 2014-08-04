#!/usr/bin/env python 
import MySQLdb as mdb
import cgi
import yate
from GenePic import *
from TFBS_tools import print_tfbs

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene_id').upper()

print(yate.start_response())
print(yate.include_header("Your SNPs, served fresh and hot!"))  

genes = GenePic(form_data)

with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    genes.setcursor(cur)
    cur.execute( """SELECT  TFBS.TFBS_ID   FROM    TFBS,GENE,GENE2TFBS 
                                WHERE  GENE.gene_id = %s
                                AND  GENE.gene_id = GENE2TFBS.gene_id
                                AND GENE2TFBS.TFBS_ID = TFBS.TFBS_ID """ % (form_data))
    rows = cur.fetchall()
    temp = []
    for row in rows:
        temp.append(row['TFBS_ID'])
        genes.addTFBS(row['TFBS_ID'])

    genes.drawpic()
    print'<br><br>'
    print_tfbs(temp)
print(yate.include_footer(""))

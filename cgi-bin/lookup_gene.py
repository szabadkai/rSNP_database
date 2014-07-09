#!/usr/bin/env python 

import MySQLdb as mdb
import cgi
import yate
from GenePic import *
from TFBS_tools import print_tfbs

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene_id')

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  

genes = GenePic()

with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute( """SELECT  TFBS.TFBS_ID   FROM    TFBS,GENE,GENE2TFBS 
                                WHERE  GENE.gene_id = %s
                                AND  GENE.gene_id = GENE2TFBS.gene_id
                                AND GENE2TFBS.TFBS_ID = TFBS.TFBS_ID """ % (form_data.upper()))
    rows = cur.fetchall()
    temp = []
    for row in rows:
        temp.append(row['TFBS_ID'])
    print_tfbs(temp)

    #genes.drawpic()
print(yate.include_footer(""))

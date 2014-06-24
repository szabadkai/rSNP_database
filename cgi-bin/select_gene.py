#!/usr/bin/env python 

import MySQLdb as mdb
import cgi
import yate
from GenePic import *

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene')

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  

genes = GenePic()

with con:
    print '<div class="left fixed60perc">'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute( """SELECT DISTINCT( GENE.alt_name), GENE.gene_id    
    				FROM    GENE    
    				WHERE  GENE.alt_name LIKE '%%%s%%';""" % (form_data.upper()))

    rows = cur.fetchall()
    for row in rows:
    	print("<a href='lookup_gene.py?gene_id=%s'>%s</a>" % (row['gene_id'],row['alt_name'])),
    	print ",",
    genes.drawpic()
print("</div>")
print(yate.include_footer(""))

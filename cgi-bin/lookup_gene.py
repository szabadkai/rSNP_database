#!/usr/bin/env python 

import MySQLdb as mdb
import cgi
import yate
from GenePic import *

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene_id')

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  

genes = GenePic()

with con:
    print '<div><table><tr><td>gene</td><td>celltype</td><td>antibody</td></tr><tr>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute( """SELECT  *   FROM    HTTP,TFBS,GENE,GENE2TFBS 
                                WHERE  GENE.gene_id = %s
                                AND  GENE.gene_id = GENE2TFBS.gene_id
                                AND GENE2TFBS.TFBS_ID = TFBS.TFBS_ID 
                                AND CONCAT_WS('_','hs',TFBS.disease,TFBS.experiment)=HTTP.experiment 
                                ORDER BY TFBS.organism,GENE.gene_id,TFBS.disease,TFBS.experiment""" % (form_data.upper()))
    rows = cur.fetchall()
    for row in rows:
        row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s'target=\"_blank\">%s</a></div>" % (row['TFBS_ID'],row['TFBS_ID'],row['TFBS_ID'],row['alt_name'])
        print "<td>%s</td>" % row['TFBS_ID']
        print "<td>%s</td>" % (row['disease'])
        x = row['TFBS.experiment'].split('_')[-1]
        print "<td><a href='%s'>%s<a></td></tr>" % (row['http'],x)
	
        genes.add(row['alt_name'], row['peak_start'], row['peak_stop'], row['GENE.start'])

    print("</table></div>")
    genes.drawpic()
print(yate.include_footer(""))

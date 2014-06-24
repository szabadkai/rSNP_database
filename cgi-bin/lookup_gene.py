#!/usr/bin/env python 

import MySQLdb as mdb
import cgi
import yate


con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene')

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
    print '<div class="input_field"><table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute( """SELECT  *   FROM    HTTP,TFBS,GENE,GENE2TFBS 
                                WHERE  GENE.alt_name LIKE '%%%s%%'
                                AND  GENE.gene_id = GENE2TFBS.gene_id
                                AND GENE2TFBS.TFBS_ID = TFBS.TFBS_ID 
                                AND CONCAT_WS('_','hs',TFBS.disease,TFBS.experiment)=HTTP.experiment 
                                ORDER BY TFBS.organism,TFBS.disease,TFBS.experiment ORDER by GENE.gene_id""" % (form_data.upper()))
    rows = cur.fetchall()
    
    for row in rows:
        row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s'target=\"_blank\">%s</a></div>" % (row['TFBS_ID'],row['TFBS_ID'],row['TFBS_ID'],row['alt_name'])
        print "<th>%s</th>" % row['TFBS_ID']
        print "<th>%s %s</th>" % (row['organism'],row['disease'])
        print "<th><a href='%s'>%s<a></th></tr>" % (row['http'],row['TFBS.experiment'])
    print("</table></div>")   
print(yate.include_footer(""))

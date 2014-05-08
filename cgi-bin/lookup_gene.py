#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate


con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

form_data = cgi.FieldStorage().getvalue('gene')

header_order = ['rs_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','orto_bases'] 
header={'rs_ID' :'SNP ID' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','orto_bases':'Orthologs'}

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
    print '<div class="input_field"><table>'
    print "<thead><tr>"
    for col in header_order:
        print "<th>%s</th>" % header[col]
    print "</tr></thead>"
        

    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT  *    FROM    TFBS,GENE
                WHERE  GENE.gene = '%s' AND 
                GENE.TFBS_ID = TFBS.TFBS_ID """ % form_data)
    rows = cur.fetchall()
    
    for row in rows:
        row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s' target=\"_blank\">%s</a></div>" % ((row['TFBS_ID'],) * 4)
        print "<tr>"
        print "<th>%s</th>" % row['TFBS_ID']
        print "</tr>"
        
    print("</table></div>")   
print(yate.include_footer(""))

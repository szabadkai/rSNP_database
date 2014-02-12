#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['TFBS_ID','ORTHOLOGS.peak','de_novo_motif','organism','chr','start','stop','target_perc','p']
header = {'TFBS_ID':'TFBS','ORTHOLOGS.peak':'PEAK','de_novo_motif':'motif','organism':'Organism','chr':'chr','start':'start','stop':'stop','target_perc':'target%','p':'P'}

form_data = cgi.FieldStorage().getvalue('id')



print(yate.start_response())
print(yate.include_header(''))  
with con: 
    print '<div class="input_field"><table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS,ORTHOLOGS,HTTP 
                    WHERE experiment='%s' AND 
                    TFBS.peak = ORTHOLOGS.peak AND
                    CONCAT_WS('_',TFBS.organism,TFBS.disease,TFBS.experiment)=HTTP.experiment ;""" % form_data)
    rows = cur.fetchall()
    print "<thead>"
    for col in header_order:
        print "<th>%s</th>" % header[col]
    print "<th>GEO</th></thead>"
    for row in rows:
        print "<tr>"
        for col in header_order:
            print "<th>%s</th>" % row[col]
        print "<th><a href='%s'>LINK<a></th>" % row['http']    
        print "</tr>"
    else:
        pass
    
    print("</table></div><br>")
    print("<a href='ortho_fasta.py?peak=%s' download='%s.fa'>download peak orthologs</a><br>" % (rows[0]['peak'],rows[0]['peak']) )
print(yate.include_footer({""}))


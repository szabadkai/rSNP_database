#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['TFBS_ID','peak','de_novo_motif','organism','chr','start','stop','target_perc','p']
header = {'TFBS_ID':'TFBS','peak':'PEAK','de_novo_motif':'motif','organism':'Organism','chr':'chr','start':'start','stop':'stop','target_perc':'target%','p':'P'}

form_data = cgi.FieldStorage().getvalue('exp')



print(yate.start_response())
print(yate.include_header(''))  
print(yate.para(form_data))
with con: 
    print '<div class="input_field"><table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS,HTTP 
                    WHERE TFBS.experiment='%s' AND 
                    CONCAT_WS('_',TFBS.organism,TFBS.disease,TFBS.experiment)=HTTP.experiment order by chr limit 1 ;""" % form_data)
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

    
    print("</table></div><br>")
    print("<a href='export2bed.py?exp=%s' download='%s.bed'>download bed</a><br>" % (form_data,form_data) )

print(yate.include_footer({""}))


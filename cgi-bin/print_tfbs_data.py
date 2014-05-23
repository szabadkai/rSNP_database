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

header_order = ['TFBS_ID','ORTHOLOGS.peak','de_novo_motif','organism','chr','start','stop','target_perc','p']
header = {'TFBS_ID':'TFBS','ORTHOLOGS.peak':'PEAK','de_novo_motif':'motif','organism':'Organism','chr':'chr','start':'start','stop':'stop','target_perc':'target%','p':'P'}

form_data = cgi.FieldStorage().getvalue('id')



print(yate.start_response())
print(yate.include_header(''))  
with con: 
    print '<div class="input_field"><table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS,ORTHOLOGS,HTTP 
                    WHERE TFBS_ID='%s' AND 
                    TFBS.peak = ORTHOLOGS.peak AND
                    CONCAT_WS('_','hs',TFBS.disease,TFBS.experiment)=HTTP.experiment 
                    ;""" % str(form_data))
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
   
    #######################################################


    header_order = ['rs_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','orto_bases','matrix_id'] 
    header={'rs_ID' :'SNP ID' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','orto_bases':'Orthologs','matrix_id':'MATRIX'}
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT RS.* ,TFBS.TFBS_ID,TFBS.matrix_id, TFBS.start, TFBS.stop, TFBS.strand
                    FROM TFBS,RS 
                    WHERE TFBS.TFBS_ID='%s' AND TFBS.TFBS_ID = RS.TFBS_ID""" % form_data)

    rows = cur.fetchall()

    if len(rows)>0:
        print '<div class="input_field"><table>'
        print "<thead><tr>"
        for col in header_order:
            print "<th>%s</th>" % header[col]
        print "</tr></thead>"

        
            
        for row in rows:
            if row['strand']=='-':
                pos = row['SNP_pos'],row['stop'],row['start']
            else: 
                pos = row['SNP_pos']-row['start']

            row['matrix_id']="<a href='print_matrix.py?id=%s&pos=%s&minor=%s&major=%s'>show matrix</a>" % (row['rs_ID'],pos,row['minor_al'],row['major_al'])
            row['rs_ID']= "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>%s</a><br>" % ((row['RS_num'],) * 2)
            row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s' target=\"_blank\">tfbs_%s</a></div>" % ((row['TFBS_ID'],) * 4)
            print "<tr>"
            for col in header_order:
                print "<th>%s</th>" % row[col]
            print "</tr>"
        print("</table></div>")
    else:
        print"No SNP in this TFBS"

print("<a href='ortho_fasta.py?peak=%s' download='%s.fa'>download peak orthologs</a><br>" % (rows[0]['peak'],rows[0]['peak']) )
print(yate.include_footer({""}))




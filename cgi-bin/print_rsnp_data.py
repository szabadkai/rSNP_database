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

field = cgi.FieldStorage().getvalue('SNPs')

header_order = ['rs_ID','TFBS_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','matrix_id'] 
header={'rs_ID' :'SNP ID' ,'TFBS_ID' : 'TFBS' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','matrix_id':'MATRIX'}

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
    print '<div class="input_field"><table>'
    print "<thead>"
    for col in header_order:
        print "<th>%s</th>" % header[col]
    print "</thead>"
        
    for form_data in split_input(field):
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(""" SELECT  RS.* ,TFBS.TFBS_ID,TFBS.matrix_id
                        FROM    RS, TFBS
                        WHERE   RS_num='%s' AND 
                                TFBS.TFBS_ID=RS.TFBS_ID""" % form_data)
        rows = cur.fetchall()
        
        for row in rows:
            row['matrix_id']="<a href='print_matrix.py?id=%s'>show matrix</a>" % (row['rs_ID'])
            row['rs_ID']= "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>%s</a><br>" % (row['RS_num'],row['RS_num'])
            row['TFBS_ID']="<a href='print_tfbs_data.py?id=%s'>%s</a></th>" % (row['TFBS_ID'],row['TFBS_ID'])
            print "<tr>"
            for col in header_order:
                print "<th>%s</th>" % row[col]
            print "</tr>"
        
    print("</table></div>")   
print(yate.include_footer(""))

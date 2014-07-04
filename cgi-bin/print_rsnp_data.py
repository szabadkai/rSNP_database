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

header_order = ['rs_ID','TFBS_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','similar_TFBS','matrix_id'] 
header={'rs_ID' :'SNP ID' ,'TFBS_ID' : 'TFBS' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele','similar_TFBS':'similar_TFBS', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phastcons score','matrix_id':'MATRIX'}

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
    print '<div><table><tr>'
    for col in header_order:
        print "<td>%s</td>" % header[col]
    print "</tr>"
        
    for form_data in split_input(field):
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(""" SELECT  RS.* ,TFBS.TFBS_ID,TFBS.matrix_id, TFBS.start, TFBS.stop, TFBS.strand, TFBS.similar_TFBS
                        FROM    RS, TFBS
                        WHERE   RS_num='%s' AND TFBS.TFBS_ID=RS.TFBS_ID""" % form_data)
        
        rows = cur.fetchall()
        
        for row in rows:
            if row['strand']=='-':
                pos = row['stop']-row['SNP_pos']
            else:
                pos = row['SNP_pos']-row['start']
            row['matrix_id']="<a href='print_matrix.py?id=%s&pos=%s&minor=%s&major=%s'>show matrix</a>" % (row['rs_ID'],pos,row['minor_al'],row['major_al'])
            row['rs_ID']= "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>%s</a>" % ((row['RS_num'],) * 2)
            row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s' target=\"_blank\">tfbs%s</a></div>" % ((row['TFBS_ID'],) * 4)            
            
            print "<tr>"
            for col in header_order:
                print "<td>%s</td>" % row[col]
            print "</tr>"

    print("</table></div>")   

print(yate.include_footer(""))

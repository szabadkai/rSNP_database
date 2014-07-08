#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate

organisms=('hg19','panTro2','gorGor1','ponAbe2','rheMac2','papHam1','calJac1','tarSyr1','micMur1','otoGar1','tupBel1','mm9','rn4','dipOrd1','cavPor3','speTri1','oryCun2','ochPri2','vicPac1','turTru1','bosTau4','equCab2','felCat3','canFam2','myoLuc1','pteVam1','eriEur1','sorAra1','loxAfr3','proCap1','echTel1','dasNov2','choHof1','macEug1','monDom5','ornAna1')
header_order = ['rs_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','orto_bases','matrix_id'] 
header={'rs_ID' :'SNP ID' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','orto_bases':'Orthologs','matrix_id':'MATRIX'}
con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

def split_input(field):
    a=[]
    b=[]
    for i in field.split(','):
        a.append(i.strip())
    for i in a:
        for c in i.split():
            b.append(c.strip())
    return b    

field = cgi.FieldStorage().getvalue('SNPs')

print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
        
    for form_data in split_input(field):
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(""" SELECT DISTINCT * FROM TFBS, RS WHERE TFBS.TFBS_ID IN (select TFBS_ID from RS where rs_num = '%s')  AND TFBS.TFBS_ID = RS.TFBS_ID;""" % form_data)
        rows = cur.fetchall()

        if len(rows)>0:
            print '<div class="rsnp_view"><table><tr>'
            for col in header_order:
                print "<td>%s</td>" % header[col]
            print "</tr>"

            
                
            for row in rows:
                if row['strand']=='-':
                    pos = row['stop']-row['SNP_pos']
                else:
                    pos = row['SNP_pos']-row['start']

                row['matrix_id']="<a href='print_matrix.py?id=%s&pos=%s&minor=%s&major=%s'>show matrix</a>" % (row['rs_ID'],pos,row['minor_al'],row['major_al'])
                row['rs_ID']= "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>%s</a><br>" % ((row['RS_num'],) * 2)
                row['TFBS_ID']="<div id=\"%s\"><a onclick='tfbsdata(\"%s\")' href='print_tfbs_data.py?id=%s' target=\"_blank\">tfbs%s</a></div>" % ((row['TFBS_ID'],) * 4)
                
                ######################################
                temp=[]
                count=0
                for letter in row['orto_bases']:
                    temp.append("<a href='#' title='%s'>%s</a>" % (organisms[count],letter))
                    count += 1
                row['orto_bases'] = ''.join(temp) 
                # jQueryUI to show organism in tooltip
                ######################################


                print "<tr>"
                for col in header_order:
                    print "<td>%s</td>" % row[col]
                print "</tr>"
            print("</table></div>")
        else:
            print"<br>No SNP in this TFBS<br>"

print(yate.include_footer(""))

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


print(yate.start_response())
print(yate.include_header("Here are your SNP(s), served fresh and hot!"))  


with con:
    print '<div><table><tr>'
    for col in header_order:
        print "<td>%s</td>" % header[col]
    print "</tr>"
        
    for form_data in split_input(field):
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT RS.* ,TFBS.TFBS_ID,TFBS.matrix_id, TFBS.start, TFBS.stop, TFBS.strand
                    FROM TFBS,RS 
                    WHERE TFBS.TFBS_ID= (SELECT TFBS_ID FROM TFBS WHERE TFBS.TFBS_ID = RS.TFBS_ID AND RS.rs_ID = '%s') AND TFBS.TFBS_ID = RS.TFBS_ID""" % form_data)

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

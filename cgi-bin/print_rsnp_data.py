#!/usr/bin/env python
from TFBS_tools import print_tfbs,print_rsnp
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
print(yate.include_header("Your SNPs, served fresh and hot!"))  


with con:
    rsnp = []
    tfbs = []
    for form_data in split_input(field):
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT DISTINCT TFBS_ID FROM RS WHERE rs_num = '%s';"% form_data)
        rows = cur.fetchall()

        if len(rows)>0:
            for i in rows:
                tfbs.append(i['TFBS_ID'])
        else:
            rsnp.append(form_data)
    if len(tfbs) > 0:
        print_tfbs(tfbs)
    elif len(rsnp) > 0:
        print_rsnp(rsnp)
    else:
        print "you are out of luck... :( \nTry arain if you will!"
print(yate.include_footer(""))

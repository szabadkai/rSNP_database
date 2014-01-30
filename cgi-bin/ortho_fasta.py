#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb 
import cgi
import yate

def export_ort(line):
    ID,TFBS,ORT=line.split(';')
    for i in range(len(header)):
        if len(ORT.split(',')[i])>40: 
            print(">"+header[i])
            print(ORT.split(',')[i])

header=('hg19','panTro2','gorGor1','ponAbe2','rheMac2','papHam1','calJac1','tarSyr1','micMur1','otoGar1','tupBel1','mm9','rn4','dipOrd1','cavPor3','speTri1','oryCun2','ochPri2','vicPac1','turTru1','bosTau4','equCab2','felCat3','canFam2','myoLuc1','pteVam1','eriEur1','sorAra1','loxAfr3','proCap1','echTel1','dasNov2','choHof1','macEug1','monDom5','ornAna1')

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

data=[]

form_data = cgi.FieldStorage().getvalue('peak')
with con:
    cur = con.cursor()
    cur.execute("SELECT data FROM ORTHOLOGS WHERE peak='%s';" % form_data)
    data.append(cur.fetchone()[0])

print(yate.start_response())      
for i in data:
    export_ort(i)
print(yate.include_footer())

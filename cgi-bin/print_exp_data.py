#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate
from TFBS_tools import print_tfbs


con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['TFBS_ID','peak','de_novo_motif','organism','chr','start','stop','target_perc','p']
header = {'TFBS_ID':'TFBS','peak':'PEAK','de_novo_motif':'motif','organism':'Organism','chr':'chr','start':'start','stop':'stop','target_perc':'target%','p':'P'}

form_data = cgi.FieldStorage().getvalue('exp')



print(yate.start_response())
print(yate.include_header(''))  
print(yate.para(form_data+" <a href='export2bed.py?exp=%s' download='%s.bed'>download bed</a><br>" % (form_data,form_data) ))
with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(" SELECT TFBS_ID FROM TFBS WHERE TFBS.experiment='%s' ORDER BY chr;" % form_data)
    rows = cur.fetchall()
    temp=[]
    for row in rows:
        temp.append(row['TFBS_ID'])

    print_tfbs(temp)

print(yate.include_footer({""}))


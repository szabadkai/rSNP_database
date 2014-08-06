#!/usr/bin/env python

import MySQLdb as mdb
import cgi
import yate
from TFBS_tools import print_tfbs, print_intervall
from pybedtools import BedTool

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['TFBS_ID','peak','de_novo_motif','organism','chr','start','stop','target_perc','p']
header = {'TFBS_ID':'TFBS','peak':'PEAK','de_novo_motif':'motif','organism':'Organism','chr':'chr','start':'start','stop':'stop','target_perc':'target%','p':'P'}

form_data = cgi.FieldStorage().getvalue('exp')
user_file = cgi.FieldStorage().getvalue('user')
mypath='/var/www/rsnpdb/DATA/BED/'+form_data+'.bed'

a = BedTool(user_file)
b = BedTool(mypath)

result = []
for line in BedTool.intersect(a,b):
	result.append(str(line).split())
print(yate.start_response())
print(yate.include_header(''))  

for line in result:
	print_intervall("'"+line[0][3:].lower()+"'",line[1],line[2])

print(yate.include_footer({""}))


#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import yate
import tempfile
import os
from pybedtools import BedTool

def putToTmp(f):
	# upload a file and store it in tmp with unique name (avoid name collision)
	tmp = tempfile.NamedTemporaryFile(delete=False)
	# TODO check the content!
	while 1:
		piece = f.file.read(10000)
		if not piece: break
		tmp.write(piece)
	tmp.close()
	return tmp.name

# processing the uploaded file
form_data = cgi.FieldStorage()

bedfile = form_data['bed']

if form_data.getvalue('jaccard'):
	jaccard = float(form_data.getvalue('jaccard').replace(',','.'))
else:
	jaccard = 0.01

tmpname = putToTmp(bedfile) # get the name of the tmp file

# # SQL query

# con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

# with con:
#     cur = con.cursor(mdb.cursors.DictCursor)
#     cur.execute(""" SELECT * FROM TFBS,HTTP 
#                     WHERE TFBS.experiment='%s' AND 
#                     CONCAT_WS('_','hs',TFBS.disease,TFBS.experiment)=HTTP.experiment order by chr;""" % form_data['bed'])
#     rows = cur.fetchall()

# HTML output

print(yate.start_response())
print(yate.include_header('')) 
 
userfile = BedTool(tmpname).sort()
mypath='/var/www/rsnpdb/DATA/BED/'
onlyfiles = [ f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]
scores=dict()

print "<p>The following experiments show higher jaccard score than <strong>%s</strong> with your experiment:</p>" % jaccard
print "<table><tr><td>Experiment</td><td>jaccard score</td></tr>"


for bed in onlyfiles:
		a = BedTool(mypath+bed)
		jac=BedTool.jaccard(userfile,a)
		if jac['jaccard']>jaccard:
			scores[bed]=jac['jaccard']

for bed in sorted(scores.items(), key=lambda x: x[1])[::-1]:
	print "<tr><td><a href='print_exp_data.py?exp=%s'>%s</a></td><td>%s</td></tr>"% (str(bed[0]).split('.')[0],bed[0],bed[1])

print"</table>"
print(yate.include_footer({""}))

# clean up mess
os.remove(tmpname)


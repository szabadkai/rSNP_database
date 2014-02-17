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
#jaccard = form_data.getvalue('jaccard')

tmpname = putToTmp(bedfile) # get the name of the tmp file

# HTML output

print(yate.start_response())
print(yate.include_header(''))  

userfile = BedTool(tmpname)
mypath='/var/www/rsnpdb/DATA/BED/'
onlyfiles = [ f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]

#print"The following experiments show higher jaccard score than <strong>%s</strong>:" % jaccard

for bed in onlyfiles:
	try:
		a = BedTool(mypath+bed)
		jac=BedTool.jaccard(userfile,a)
		if jac['jaccard']>0.4:
			print "%s\t%s<br>"% (bed,jac['jaccard'])
	except:
		print "problem in :"+bed
		pass

print(yate.include_footer({""}))

# clean up mess
os.remove(tmpname)


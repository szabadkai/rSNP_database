#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import yate
import tempfile
import os
from pybedtools import BedTool
from os import listdir
from os.path import isfile, join

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
#jaccard = float(form_data['jaccard'])

tmpname = putToTmp(bedfile) # get the name of the tmp file

# HTML output

print(yate.start_response())
print(yate.include_header(''))  

userfile = BedTool(tmpname)
mypath=os.getcwd()+'/DATA/BED/'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for bed in onlyfiles:
	try:
		a = BedTool(mypath+bed)
		jac=BedTool.jaccard(userfile,a)
<<<<<<< HEAD
		print"The following experiments show higher jaccard score than <strong>%s</strong>:" % jaccard
		if jac['jaccard']>jaccard:
			print "<a href='print_exp_data.py?exp=%s'>%s</a>\t%s\t%s\t%s<br>"% (bed,bed,jac['intersection'],jac['union-intersection'],jac['jaccard'])
=======
		if jac['jaccard']>0.4:
			print "%s\t%s\t%s\t%s<br>"% (bed,jac['intersection'],jac['union-intersection'],jac['jaccard'])
>>>>>>> 473947513b97a68a9944db07b21aa7710d76c1b4
	except:
		print "problem in :"+bed
		pass

print(yate.include_footer({""}))

# clean up mess
os.remove(tmpname)


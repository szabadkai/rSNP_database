#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

with con: 
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute(""" SELECT DISTINCT experiment FROM TFBS """)
	exp = cur.fetchall()
	for i in exp:
	    cur = con.cursor(mdb.cursors.DictCursor)
	    cur.execute(""" SELECT chr,peak_start,peak_stop FROM TFBS 
	                    WHERE TFBS.experiment='%s' order by chr ;""" % i['experiment'])
	    rows = cur.fetchall()
	    a=open('../DATA/BED/'+i['experiment']+'.bed','w')
	    for row in rows:
	        a.write( "%s\t%s\t%s\n" % (row['chr'],row['peak_start'],row['peak_stop']))
	    else:
	        pass
	    a.close()

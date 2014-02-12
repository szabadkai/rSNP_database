import MySQLdb as mdb
import cgi
import yate

con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');

header_order = ['chr','start','stop','peak']
header = {'peak':'PEAK','chr':'chr','start':'start','stop':'stop'}

form_data = cgi.FieldStorage().getvalue('exp')



print(yate.start_response())

with con: 
    print '<div class="input_field"><table>'
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM TFBS,HTTP 
                    WHERE TFBS.experiment='%s' AND 
                    CONCAT_WS('_',TFBS.organism,TFBS.disease,TFBS.experiment)=HTTP.experiment order by chr ;""" % form_data)
    rows = cur.fetchall()

    for row in rows:
        print "<tr>"
        for col in header_order:
            print "<th>%s</th>" % row[col]
        print "<th><a href='%s'>LINK<a></th>" % row['http']    
        print "</tr>"
    else:
        pass
    
    print("</table></div><br>")
print(yate.include_footer({""}))

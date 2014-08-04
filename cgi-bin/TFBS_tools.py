def print_tfbs(tfbs_IDs):
    import MySQLdb as mdb
    con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');
    #from mysql_open import *
    organisms=('hg19','panTro2','gorGor1','ponAbe2','rheMac2','papHam1','calJac1','tarSyr1','micMur1','otoGar1','tupBel1','mm9','rn4','dipOrd1','cavPor3','speTri1','oryCun2','ochPri2','vicPac1','turTru1','bosTau4','equCab2','felCat3','canFam2','myoLuc1','pteVam1','eriEur1','sorAra1','loxAfr3','proCap1','echTel1','dasNov2','choHof1','macEug1','monDom5','ornAna1')
    header_order_tfbs = ['TFBS_ID','de_novo_motif','chr','start','stop','similar_TFBS', 'target_perc','p','disease','experiment','GEO','orthologs','snp_count']
    header_tfbs = {'disease':'celltype','experiment':'antibody','snp_count':'SNP count','GEO':'GEO','orthologs':'peak orthologs','TFBS_ID':'TFBS','ORTHOLOGS.peak':'PEAK','de_novo_motif':'motif', 'chr':'chr','start':'start','similar_TFBS':'similar_TFBS' ,'stop':'stop','target_perc':'target%','p':'P'}

    print '<table id="MyTable" class="tablesorter">'
    print "<thead class='header'><tr>"
    for col in header_order_tfbs:
        print "<th>%s</th>" % header_tfbs[col]
    print "</tr></thead><tbody>"
    for tfbs_ID in tfbs_IDs:
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute(""" SELECT COUNT(RS.rs_ID)
                            FROM TFBS,RS
                            WHERE TFBS.TFBS_ID='%s' AND TFBS.TFBS_ID = RS.TFBS_ID""" % tfbs_ID)

            snp_count = cur.fetchone()['COUNT(RS.rs_ID)']

            cur.execute(""" SELECT * FROM TFBS,ORTHOLOGS,HTTP 
                            WHERE TFBS_ID='%s' AND 
                            TFBS.peak = ORTHOLOGS.peak AND
                            CONCAT_WS('_','hs',TFBS.disease,TFBS.experiment)=HTTP.experiment 
                            ;""" % tfbs_ID)
            rows = cur.fetchall()
            for row in rows:
                row['experiment'] = row['experiment'].split('_')[-1]
                row['TFBS_ID']="tfbs%s"%(row['TFBS_ID'])
                row['GEO']= "<a href='%s'>LINK<a>" % row['http']
                row['orthologs'] = "<a href='ortho_fasta.py?peak=%s' download='%s.fa'>download peak orthologs</a>" % (rows[0]['peak'],rows[0]['peak'])
                row['snp_count'] = snp_count
                print "<tr class='tfbs_view' id='%s'>" % rows[0]['TFBS_ID']
                for col in header_order_tfbs:
                    print "<td>%s</td>" % row[col]
            print "</tr>"
            id=row['TFBS_ID']

           
            #######################################################


            header_order = ['rs_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','orto_bases','matrix_id'] 
            header={'rs_ID' :'SNP ID' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','orto_bases':'Orthologs','matrix_id':'MATRIX'}
            
            cur.execute(""" SELECT RS.*,TFBS.*
                            FROM TFBS,RS 
                            WHERE TFBS.TFBS_ID='%s' AND TFBS.TFBS_ID = RS.TFBS_ID""" % tfbs_ID)

            rows = cur.fetchall()
            
            if len(rows)>0:
                print "<tr class='rsnp_view expand-child' id='%s'><td colspan=13 ><table><thead><tr>" % (id)
                for col in header_order:
                    print "<th>%s</th>" % header[col]
                print "</tr></thead><tbody>"             
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
                print "</tbody></table></td></tr>"
            else:
                pass

    print("</tbody></table>")

def print_rsnp(rs_nums):
    header_order = ['rs_ID','major_al', 'minor_al', 'freq_major', 'freq_min','rSNP_phastcons','orto_bases'] 
    header={'rs_ID' :'SNP ID' , 'freq_major':'F Major', 'freq_min':'F Minor','major_al':'MAJOR allele', 'minor_al':'MINOR allele','rSNP_phastcons' :'SNP phascons score','orto_bases':'Orthologs','matrix_id':'MATRIX'}
    organisms=('hg19','panTro2','gorGor1','ponAbe2','rheMac2','papHam1','calJac1','tarSyr1','micMur1','otoGar1','tupBel1','mm9','rn4','dipOrd1','cavPor3','speTri1','oryCun2','ochPri2','vicPac1','turTru1','bosTau4','equCab2','felCat3','canFam2','myoLuc1','pteVam1','eriEur1','sorAra1','loxAfr3','proCap1','echTel1','dasNov2','choHof1','macEug1','monDom5','ornAna1')
    import MySQLdb as mdb
    con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');
    cur = con.cursor(mdb.cursors.DictCursor)
    print "<table><tr>"
    for col in header_order:
        print "<td>%s</td>" % header[col]

    for rs_num in rs_nums:
        i=rs_num
        cur.execute(""" SELECT * FROM RS WHERE rs_num = %s;""" % i)
        rows = cur.fetchall()

      
        print "</tr>"             
        for row in rows:
            row['rs_ID']= "<a href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>%s</a><br>" % ((row['RS_num'],) * 2)
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
    print "</table>"

def print_intervall(chrom,start,stop):
    import MySQLdb as mdb
    con = mdb.connect('genome', 'rsnp', 'RSNP', 'testdb');
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(" SELECT TFBS_ID FROM TFBS WHERE chr = %s AND start BETWEEN %s and %s OR stop BETWEEN %s and %s ;" % (chrom,start,stop,start,stop))
    rows = cur.fetchall()
    temp=[]
    for row in rows:
        temp.append(row['TFBS_ID'])
    return temp 


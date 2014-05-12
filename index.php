<!DOCTYPE html>

<html>
    <head>
   <meta charset="utf-8">
   <title>rSNP database</title>
   <link rel="stylesheet" href="./main.css">
    </head>
    <body>
   <div class="topbar">
   <div class="logo">
  <a href="http://emboss.abc.hu/rsnpdb/"><img src="logo2.png" alt="logo-rsnpdb" height="40"></a>
   </div>
   </div>
   <div>
   <p id="sidebar">
 A Single Nucleotide - polymorphism (SNP, pronounced snip; plural snips) is a DNA sequence variation occurring when a Single Nucleotide — A, T, C or G — in the genome (or other shared sequence) differs between members of a biological species or paired chromosomes. For example, two sequenced DNA fragments from different individuals, AAGCCTA to AAGCTTA, contain a difference in a single nucleotide. In this case we say that there are two alleles. Almost all common SNPs have only two alleles. The genomic distribution of SNPs is not homogenous; SNPs occur in non-coding regions more frequently than in coding regions or, in general, where natural selection is acting and fixating the allele of the SNP that constitutes the most favorable genetic adaptation. Other factors, like genetic recombination and mutation rate, can also determine SNP density.
   </p>
   </div>
  
   <div class="container">
  <form action="./cgi-bin/print_rsnp_data.py" method="POST" enctype="application/x-www-form-urlencoded">
  Please let us know whitch SNP you're interested in? ( use rs# notation! )<br>
  <textarea id="seq" class="reset" rows="3" cols="80" name="SNPs">rs1000002 rs1000016 rs10000171 rs10000226  rs10000232"</textarea><br>
  <input type=submit value="Select"></form>
 <br><br>
  <form action="./cgi-bin/print_exp_data.py" method="GET" enctype="application/x-www-form-urlencoded">
   <select id="exp" name="exp" >

      <?php
      $txt_file    = file_get_contents('./DATA/exp.txt');
      $rows        = explode("\n", $txt_file);

      foreach($rows as $row => $data){
         //get row data
         echo $row;
      }
      ?>

   </select>  
     <input type=submit value="Select"></form>
   <br><br>
   <form action="./cgi-bin/uploadbed.py" enctype="multipart/form-data" method="post">
   Upload you BED file to compare with other Chip-seq experiments.<br>
    <input type="file" id="bed" name="bed" value="Upload BED file">
    <input type="text" id="jaccard" name="jaccard">
   <input type="submit" value="Upload and run analysis"><br><br><br>
   </form>
   <form action="./cgi-bin/lookup_gene.py" enctype="multipart/form-data" method="POST">
   Choose your gene of interest!<br>
   <input type="text" id="gene" name="gene">
   <input type="submit" value="submit">

   </form>
   </div>
</body></html>


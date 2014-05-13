<!DOCTYPE html>

<html>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>
<script src=".js/rsnp.js"></script>

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
         <?php echo file_get_contents('./DATA/sidebar.txt'); ?>
      </p>
   </div>
  
   <div class="container">
  <form action="./cgi-bin/print_rsnp_data.py" method="POST" enctype="application/x-www-form-urlencoded">
  Please let us know whitch SNP you're interested in? ( use rs# notation! )<br>
  <textarea id="seq" class="reset" rows="3" cols="80" name="SNPs">rs1000002 rs1000016 rs10000171 rs10000226  rs10000232</textarea><br>
  <input type=submit value="Select"></form>
 <br><br>
  <form action="./cgi-bin/print_exp_data.py" method="GET" enctype="application/x-www-form-urlencoded">
   <select id="exp" name="exp" >

      <?php
      $txt_file    = file_get_contents('./DATA/exp.txt');
      $rows        = explode("\n", $txt_file);

      foreach($rows as $row){
         //get row data
         echo $row;
      }
      ?>

   </select>  
     <input type=submit value="Select"></form>
   <br><br>
   <form action="./cgi-bin/uploadbed.py" enctype="multipart/form-data" method="post">
  Upload you BED file to compare with other Chip-seq experiments.<br>
  <input type="file" id="bed" name="bed" value="Upload BED file"><br>

<div class="tiptext">Text
<div class="description"> Here is the big fat description box</div>
</div>





    Jaccard score: 
    
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


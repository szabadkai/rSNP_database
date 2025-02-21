<!DOCTYPE html>

<html>
  <head>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
    <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
    <script type="text/javascript" src='js/rsnp.js'></script>
    <meta charset="utf-8">
    <title>rSNP database</title>
    <link rel="stylesheet" href="./main.css">
     <script>
    $(function() {
    $( document ).tooltip();
    });
    $(function() {
    $( "#accordion" ).accordion();
    });
    $(function() {
    $( "#tabs" ).tabs();
    });
    </script>
    </head>
    <body>

<div class="topbar">
  <div class="logo">
     <a href="http://emboss.abc.hu/rsnpdb/"><img src="logo2.png" alt="logo-rsnpdb" height="40"></a>
     <div class="white">
        collection of human regulatory single nucleotide polimorfisms from chip-seq data
     </div>
  </div>
</div>

<div id="tabs">
  <ul>
    <li><a href="#tabs-1">SNP view</a></li>
    <li><a href="#tabs-2">BED view</a></li>
    <li><a href="#tabs-3">Gene view</a></li>
    <li><a href="#tabs-4">Region view</a></li>
  </ul>
  <div id="tabs-1">
    <form action="./cgi-bin/print_rsnp_data.py" method="POST" enctype="application/x-www-form-urlencoded">
      Please let us know whitch SNP you're interested in? ( use rs# notation! )<br>
      <textarea id="seq" class="reset" rows="3" cols="80" name="SNPs">rs1000002 rs1000016 rs10000171 rs10000226  rs10000232</textarea><br>
      <input type=submit value="Select"></form>
      </div>
  <div id="tabs-2">
    <form action="./cgi-bin/uploadbed.py" enctype="multipart/form-data" method="post">
      Upload you BED file to compare with other Chip-seq experiments.<br>
      <input type="file" id="bed" name="bed" value="Upload BED file"><br>
      <a href="#" title="The Jaccard index, also known as the Jaccard similarity coefficient 
      (originally coined coefficient de communauté by Paul Jaccard), is a statistic used for 
      comparing the similarity and diversity of sample sets.">Jaccard score</a>:
      <input type="text" id="jaccard" name="jaccard">
      <input type="submit" value="Upload and run analysis"><br><br><br>
      </form>
      </div>
  <div id="tabs-3">
    <form action="./cgi-bin/select_gene.py" enctype="multipart/form-data" method="POST">
      Choose your gene of interest!<br>
      <input type="text" id="gene" class="reset" rows="1" cols="50" name="gene" value="HLA"><br>
      <input type=submit value="Select">
      </form>
      </div>
<div id="tabs-4">
	Specify region you are interested in!<br>
	<form action='./cgi-bin/select_region.py' method="POST" enctype="application/x-www-form-urlencoded">
    <select name="chr" id='chr'>
      <?php
        $sample= range(1,22);
        $sample[] = 'X';
        $sample[] = 'Y';
        foreach($sample as $i){
        	echo "<option value='".$i."'>chr".$i."</option>";
        }
      ?>
    </select> 
    from: <input type="number" name="start" id='start'> to: <input type='number' name="stop" id='stop'>
    <br><input type="submit" value="Select">
  </form>
</div>
</div>
</body></html>


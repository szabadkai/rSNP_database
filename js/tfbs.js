$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".tfbs_view").on("click", function(){
		$(this).next(".rsnp_view").slideToggle();
	});
	$("#MyTable").tablesorter(); 
});

$("thead").on("click",function(){
         setTimeout(function(){
		 $('.tfbs_view').each(function() {
                	var currentId = $(this).attr('id');
                	$(".rsnp_view#"+currentId).insertAfter(".tfbs_view#"+currentId);
       		 });

	}, 500);  

});



$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".tfbs_view").on("click", function(){
		$(this).next(".rsnp_view").slideToggle();
	});
	$("#MyTable").tablesorter(); 
	$('.tfbs_view').each(function() {
		var currentId = $(this).attr('id');
		$("#"+currentId).insertAfter($(this))
	});

});

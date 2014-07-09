$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".tfbs_view").on("click", function(){
		$(this).last().find(".rsnp_view").slideToggle();
	});
});
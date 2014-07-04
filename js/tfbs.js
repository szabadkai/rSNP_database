$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".tfbs_view").on("click", function(){
		$(this).parent().find(".rsnp_view").slideToggle();
	});
});
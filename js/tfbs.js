$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".tfbs_view").on("click", function(){
		$(this).next('.rsnp_view').slideToggle();
	});
});
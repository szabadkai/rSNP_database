$(document).ready(function() {
	$(".rsnp_view").hide();

	$(".rsnp_view").on("click", function(){
		$(this).slideToggle();
	});
});
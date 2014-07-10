$(document).ready(function() {
	$(".rsnp_view").css("height:0px");

	$(".tfbs_view").on("click", function(){
		$(this).next().animate("height:50px");
	});
});
// function tfbsdata(tfbsid){
//    div = document.getElementById(tfbsid);
//    div.style.width  = 200 + "px";
//    div.style.height = 200 + "px";
// }

//window.onload = function(){
//  alert("It is working");
//}
$(".tiptext").mouseover(function() {
    $(this).children(".description").show();
}).mouseout(function() {
    $(this).children(".description").hide();
});

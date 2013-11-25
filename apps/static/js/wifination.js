function showInvalid(){
   $("p#failed_").fadeIn("slow").removeClass('hide');
}
function submitForm(){
  return;
   var ok = true;
   if ($("input#login_username").val() === ""){
      ok = false;
      $("div#frmgrp-username").addClass("has-error");
      showInvalid();
   }if ($("input#login_password").val() === ""){
      ok = false;
      $("div#frmgrp-password").addClass("has-error");
      showInvalid();
   }
   if (ok){$("form#login_form").submit()}
}
function resolveFullHeight() {
  $("#imgs-div").css("height", "auto");

  var h_window = $(window).height(),
    h_document = $(document).height(),
    fullHeight_top = $("#imgs-div").position().top,
    est_footerHeight = 50;

  var h_fullHeight = (-1 * (est_footerHeight + (fullHeight_top - h_document)));

  $("#imgs-div").height(h_fullHeight);
}
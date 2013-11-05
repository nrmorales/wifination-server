function showInvalid(){
   $("p#failed_").fadeIn("slow").removeClass('hide');
}
function submitForm(){
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
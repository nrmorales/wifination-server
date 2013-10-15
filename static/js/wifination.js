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
$("button#btn-login").click(function(){
   $('div#input_.hide').fadeIn("slow").removeClass('hide');
   $("button#btn-login").text("Login Now!");
   $("button#btn-login").attr('onclick','').click(submitForm);
});
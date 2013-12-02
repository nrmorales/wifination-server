/* facebook authentication related script
 * this code in inserted in landing page <body> 
 * @author: Ivan Baguio
 */

window.fbAsyncInit = function() {
   /* facebook app initialization*/
   FB.init({
      appId      : '248863558597971', 
      channelUrl : 'static/channel.html', 
      status     : true,
      cookie     : true,
      xfbml      : true 
   });
   /* event handler for auth response */
   FB.Event.subscribe('auth.authResponseChange', function(response) {
      console.log("responsechange");
      if (response.status === 'connected') {
         if (!window.isClicked){ //user is already logged connected to facebook
            showWelcomeUser();    //show welcome button to have user login
         }else{
            doLogin();
         }
      }/* else if (response.status === 'not_authorized') {
         doFbLogin();
      }*/ else {
         doFbLogin();
      }
   });

   /* query login status of user from facebook */
   FB.getLoginStatus(function(response) {
      if (response.status === 'connected') {
         showWelcomeUser()
      } else {
         showLoginUser()
      }
   });
};
// Load the SDK asynchronously
(function(d){
   console.log("loading SDK asynchronously")
   var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement('script'); js.id = id; js.async = true;
   js.src = "//connect.facebook.net/en_US/all.js";
   ref.parentNode.insertBefore(js, ref);
}(document));
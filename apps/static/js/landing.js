var isClicked = false;
   /* queries fb for user info,and submits form */
   function doLogin(){
      FB.api("/me", function(response){
        var keys = ["id","first_name","last_name","gender",
        "hometown","link","location","username","email","education"]
        console.log("setting form info");
        $("[name='username']").val("wifinationuser")
        $("[name='password']").val("randomstring")
        if (response.email) $("[name='email']").val(response.email)
        var xy = {};
        for (var key in response){
          if (keys.indexOf(key) >= 0)
            xy[key] = response[key]
            //console.log(key)
        }
        console.log(response)
        console.log(JSON.stringify(xy))
        console.log("submitting form");
        showForm();
        //$("#login_form").submit();
      });
   }

   function verifyUser(){
      FB.api(".me", function(response){
        
      });

      FB.api("/me", function(response){
        var keys = ["id","first_name","last_name","gender",
        "hometown","link","location","username","email","education"]
        var xy = {};
        for (var key in response){
          if (keys.indexOf(key) >= 0)
            xy[key] = response[key]
        }

        $.ajax({
          type : "POST",
          url : "//localhost/wifination/cgi/verify",
          data: JSON.stringify(xy, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(result) {
              console.log(result);
          }
        });
      });
   }
   //show the form details on the log
   function showForm(){
      var x = $("#login_form");
      console.log(x.serializeArray());
   }

   /* adding functionality to buttons */
   $("button.btn-login").bind("click",function(){
    doFbLogin() //add click function to login button
    });
   $("a#logout-user").bind("click", function(){
      FB.logout(function(response){ showLoading()})
   });
   $("button#btn-continue").bind("click",function(){
      doLogin()
   });

   function showLoading(msg){
      $('img.img-loading').fadeIn(function(){
        $('button.btn-login').hide();
        $('div#logged-user-div').hide();
        if (msg){
          $('.loading-msg').text(msg)
        }else
          $('.loading-msg').text("")
      });
   }

   function showWelcomeUser(){
      console.log("welcoming user")
      FB.api('/me', function(response) {
         console.log(response)
         $("span#user-name").text(response.first_name)
         $('img#user-pic').attr('src','//graph.facebook.com/'+response.id+'/picture')
         $('img.img-loading').fadeOut(function(){
            $('div#logged-user-div').css('visibility','visible').fadeIn().removeClass('hidden');
            $('button.btn-login').hide();
         });
         /* check if user already is registered in */
         $.ajax({
          type : "POST",
          url : "//localhost/wifination/cgi/verify",
          data: JSON.stringify({'username':response['username']}, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(result) {
              if (result === 'exists'){
                
              }
          }
        });
      })
   }

   /* user is not logged in to fb or has not 
      yet authorized wifination show connect button */
   function showLoginUser(){
      $("input[name='newuser']").val('true')
      console.log("user not yet connected")
      $('img.img-loading').fadeOut(function(){
         $('button.btn-login').css('visibility','visible').fadeIn().removeClass('hidden');
         $('div#logged-user-div').hide();
      });
   }

   /* query facebook for user to login and use app */
   function doFbLogin(){
      FB.login(function(response){
         //fb_publish();
         doLogin()
      }/*, {scope:'email,publish_actions'}*/);
   }

  function fb_publish() {
   FB.ui({
       method: 'stream.publish',
       message: 'Test',
       attachment: {
         name: 'Test:Name',
         caption: 'Test:Caption',
         description: (
           'Test:description here'
         ),
         href: 'http://wifination.ph'
       },
       action_links: [
         { text: 'Test:Code', href: 'http://wifination.ph/action' }
       ],
       user_prompt_message: 'Tell your friends blah blah'
     },
     function(response) {
       if (response && response.post_id) {
         console.log('Post was published.');
       } else {
         console.log('Post was not published.');
       }
     }
   );  
  }
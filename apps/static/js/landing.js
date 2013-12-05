var isClicked = false;
   /* queries fb for user info,and submits form */
   function doLogin(){
      FB.api("/me", function(response){
        var keys = ["id","first_name","last_name","gender",
        "hometown","link","location","username","email","education"]
        console.log("setting form info");
        $("[name='username']").val("wifinationuser");
        $("[name='password']").val("randomstring");
        verifyUser()
      });
   }
   /* checks if the user is already created in the server, if not
      it sends a request to create it */
   function verifyUser(){
      FB.api("/me", function(response){
        console.log("kox")
        var keys = ["id","first_name","last_name","gender",
        "hometown","link","location","username","email","education"]
        var info = {};
        for (var key in response){
          if (keys.indexOf(key) >= 0)
            info[key] = response[key]
        }
        console.log(info)
        $.ajax({
          type : "POST",
          url : "/wifination/cgi/verify",
          data: JSON.stringify(info, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(result) {
              console.log("result:"+result);
              if (result == "new"){
                console.log("new user. will add");
                addUserInfo(info)
              }else if(result == "exists"){
                console.log("user exists. will login");
              }
          },
          error: function(result){
            console.log("fail");
            console.log(result);
          }
        });
      });
   }
   function addUserInfo(info){
      $.ajax({
        type: "POST",
        url : "/wifination/cgi/aui",
        data: JSON.stringify(info,null,'\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          console.log(result);
          $("#login_form").submit();
        },
        error: function(result){
          console.log("error")
          console.log(result);
          $("#login_form").submit();
        }
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
          url : "/wifination/cgi/verify",
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
      }, {scope:'email,publish_actions'});
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
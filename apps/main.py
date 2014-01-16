from flask import Flask
from flask import render_template as render
from flask import request, make_response, url_for, redirect
from flask_mobility import Mobility

import hashlib, urllib, database
from admin import *

app = Flask(__name__)
app.debug = True
Mobility(app)

#constant variables
uamsecret = "uamsecret"

@app.route("/test-old")
def login3():
   return render("landingpage.html",page_vars={})

@app.route("/test-hub")
def login33():
   return render("surveypage-coffeehub.html",page_vars={})

@app.route("/test-new")
def login2():
   return render("landingpage-new.html",page_vars={})

@app.route("/test-demo")
def tdemo():
   return render("surveypage-demo.html",page_vars={})

@app.route("/test-manila")
def tdemo2():
   return render("landing-manila.html",page_vars={})

@app.route("/test-manila-survey")
def tdemo3():
   if request.MOBILE:
      return render("surveypage-manila-mobile.html",page_vars={})
   else:
      return render("surveypage-manila.html",page_vars={})

@app.route("/test-synetcom")
def tdemo4():
   return render("surveypage-synetcom.html",page_vars={})

@app.route("/test/redirect")
def redir():
   if request.MOBILE:
      return render("redirecting-mobile.html", page_vars={})
   return render("redirecting.html", page_vars={})

@app.route("/test/redirect-mob")
def redir2():
   return render("redirecting-mobile.html", page_vars={})

@app.route('/img/<filename>')
def serveImage(filename):
   return url_for('static', filename=filename)

@app.route('/test/ads')
def testAds():
   return render("redirecting.html", page_vars={})

#stores primary info of user
#aui = add user info
@app.route('/cgi/aui',methods=["POST"])
def addUserInfo():
   uname = request.json['username']
   #remove username from json
   info = {key: value for key, value in request.json.items() if value is not uname}
   database.addUserInfo(uname,info)
   return "ok"

#checks if the user's primary info is already stored
@app.route('/cgi/verify',methods=["POST"])
def isRegistered():
   USER_NEW = "new"
   USER_EXISTS = "exists"
   uname = request.json['username']
   if database.userExists(uname):
      return USER_EXISTS
   return USER_NEW

@app.route('/test')
def test():
   ss = "data "+ str(request.data) +"<br/>"
   ss += "base_url " + str(request.base_url) +"<br/>"
   ss += "url_root " + str(request.url_root) +"<br/>"
   ss += "url " + str(request.url) +"<br/>"
   ss += "script_root " + str(request.script_root) +"<br/>"
   ss += "path " + str(request.path) +"<br/>"
   ss += "args " + str(request.args) +"<br/>"
   ss += "get_json " + str(request.get_json) +"<br/>"
   ss += "is_secure " + str(request.is_secure) +"<br/>"
   return ss

@app.route('/demo',methods=['GET','POST'])
@app.route('/wifination/demo',methods=['GET','POST'])
def showDemo():
   return landingpage(mode="demo")

@app.route('/demo-manila',methods=['GET','POST'])
@app.route('/wifination/demo-manila',methods=['GET','POST'])
def showDemoManila():
   return landingpage(mode="manila")

@app.route('/demo-synetcom',methods=['GET','POST'])
@app.route('/wifination/demo-synetcom',methods=['GET','POST'])
def showDemoSynetcom():
   return landingpage(mode="synetcom")

@app.route('/coffeehub',methods=['GET','POST'])
def showCoffeeHub():
   return landingpage(mode="coffeehub")

@app.route('/authenticate', methods=['GET','POST'])
@app.route('/wifination/authenticate', methods=['GET','POST'])
def landingpage(mode=None):
   if app.debug: print "processing landing page"
   def getRequestData():   #returns the get parameters
      data = {}
      try:
         for key in request.args.keys():
            data[key] = request.args[key]
         for key in request.form:
            data[key] = request.form[key]
      except Exception, e:
         print e
         raise e
      if app.debug: print "Get params:", str(data)
      return data 

   request_data = getRequestData()

   if not request.is_secure:
      if app.debug: print "Connection is NOT secure. Please connect thru HTTPS"
      #return render("simple_with_xml.html", mesg="Please connect thru HTTPS", headline="Connection is NOT secure")
      pass #show html for insecure connections
   first_cond = "res" in request_data and request_data['res'] == "wispr" and request_data['username']
   second_cond = "loginattempt" in request_data and request_data["loginattempt"] == "wifination"

   if app.debug: print "First Condition:",first_cond,"Second Condition:",second_cond
   if first_cond or second_cond:   
      hexchal = request_data["challenge"].decode("hex")
      if uamsecret: toHash = hexchal+uamsecret
      else: toHash = hexchal
      
      md5hash = hashlib.md5(toHash)
      newchal = md5hash.hexdigest()

      #url details dictionary
      lurldet =  {'uamip':request_data['uamip'], 'uamport':request_data['uamport'],
                  'username':urllib.quote_plus(request_data['username'])}

      logonUrl = "http://%(uamip)s:%(uamport)s/logon?username=%(username)s"%(lurldet)

      if all(key in request_data for key in ('wisprversion','wispreapmsg')) and request_data['wisprversion'] \
         and request_data['wispreapmsg']:
         logonUrl += "&WISPrEAPMsg="+urllib.quote_plus(request_data['wispreapmsg'])
         logonUrl += "&WISPrVersion="+urllib.quote_plus(request_data['wisprversion'])

      #did not add the ntresponse thingy, only used for MS-CHAP
      #did not add plain text thingy, only used for PAP

      # Generate a CHAP response with the password and the
      # challenge (which may have been uamsecret encoded)
      else:
         response = hashlib.md5(request_data['password']+newchal).hexdigest()
         logonUrl += "&response="+urllib.quote_plus(response)

      logonUrl += "&userurl="+urllib.quote_plus(request_data['userurl']);
      print "LoginURL:",logonUrl
      return wnredirect(logonUrl,mode)

   #another part of the script
   result = getResult(request_data)

   if app.debug: print "Result:",result

   if result == 0:
      err = """Login must be performed through CoovaChilli daemon.
      <br/><a href="demo?res=notyet&uamip=192.168.182.1&uamport=3990&challenge=1f3590180f5ef93864dcfc0f5b17a15c&userurl=http%3a%2f%2fgoogle.com&nasid=nas01&mac=E0-B9-A5-C6-59-1F">Click here</a>"""
      return error("WiFi Nation Login Failed",err)

   if result == 1:
      if app.debug: print "Logged in to WiFi Nation Success!"
      return render("simple-redirect.html",redirect_url=request_data['userurl'])

   if result == 6:
      pass

   if result == 2:
      if app.debug: print "WiFi Nation Login Failed!", request_data['reply']
      return render("landingpage.html",page_vars = {'error_msg':"WiFi Nation Login Failed"},loginpath="/wifination/authenticate")

   if result == 5:
      if app.debug: print "Not yet logged in"
      if mode == "demo":
         return render("landingpage-new.html",page_vars=request_data,loginpath="/wifination/demo")
      elif mode == "manila":
         return render("landingpage-manila.html",page_vars=request_data,loginpath="/wifination/demo-manila")
      elif mode == "coffeehub":
         return render("landingpage-new.html",page_vars=request_data,loginpath="/wifination/coffeehub")
      elif mode == "synetcom":
         return render("landingpage-new.html",page_vars=request_data,loginpath="/wifination/demo-synetcom")
      else:
         return render("landingpage-new.html",page_vars=request_data,loginpath="/wifination/authenticate")

   if result == 4 or result == 12:
      logoutUrl = """<a href="http://%(uamip)s:%(uamport)s/logoff">Logout</a>"""%(request_data)
      if app.debug: print "Logout URL:",logoutUrl
      return render("simple-redirect.html",headline="Logged in to WiFi Nation!",mesg=logoutUrl,redirect_url=request_data['userurl'])

   if result == 11:
      if app.debug: print "Logging in to WiFi Nation"
      return render("simple.html",headline="Logging in to WiFi Nation",mesg="Please wait...")

   if result == 13:
      if app.debug: print "Logged out from WiFi Nation"
      return render("simple.html",headline="Logged out from WiFi Nation",mesg="")

def wnredirect(redirect_url,mode):
   if app.debug: print "Redirecting to",redirect_url
   if mode == "demo": 
      return render("surveypage-demo.html", redirect_url=redirect_url, page_vars={}, ismobile=request.MOBILE)
   elif mode == "manila":
      if request.MOBILE:
         return render("surveypage-manila-mobile.html", redirect_url=redirect_url, page_vars={})   
      else:
         return render("surveypage-manila.html", redirect_url=redirect_url, page_vars={})
   elif mode == "synetcom":
      return render("surveypage-synetcom.html", redirect_url=redirect_url, page_vars={})
   elif mode == "coffeehub":
         return render("surveypage-coffeehub.html",redirect_url=redirect_url, page_vars={})
   if request.MOBILE:
      return render("surveypage-mobile.html", redirect_url=redirect_url, page_vars={})
   else:
      return render("surveypage.html", redirect_url=redirect_url, page_vars={})

   #return render("simple.html", redirect_url=redirect_url, mesg="Please Wait...",headline="Logging in to WiFi Nation")

def error(headline, mesg):
   if app.debug: print "Error:", headline, mesg
   return render("simple.html",headline=headline,mesg=mesg)

#returns the appropriate result code depending on the request_data['res']
def getResult(request_data):
   if "res" not in request_data: return 0
   elif request_data['res'] == "success": return 1
   elif request_data['res'] == "failed":  return 2
   elif request_data['res'] == "logoff":  return 3
   elif request_data['res'] == "already": return 4
   elif request_data['res'] == "notyet":  return 5
   elif request_data['res'] == "wispr":   return 6
   elif request_data['res'] == "popup1":  return 11
   elif request_data['res'] == "popup2":  return 12
   elif request_data['res'] == "popup3":  return 13
   return 0

@app.route('/admin-login',methods=['GET','POST'])
def login():
   if request.method == "POST":
      if request.form["username"] == "admin" and request.form["password"] == "wifination":
         response = redirect(url_for('showAdmin'))
         response.set_cookie('jklol',value='keox')
         return response
      else:
         return render("admin-login.html",page_vars={'fail':True})
   else:
      return render("admin-login.html",page_vars={})

@app.route('/admin-dashboard')
def showAdmin():
   valid = request.cookies.get('jklol')
   if valid == 'keox':
      return render("admin-dashboard.html",page_vars={})
   else:
      return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
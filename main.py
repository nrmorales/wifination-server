from flask import Flask
from flask import render_template as render
from flask import request, make_response, redirect, url_for

import hashlib, urllib

app = Flask(__name__)
app.debug = True

#constant variables
uamsecret = "uamsecret"

@app.route('/img/<filename>')
def serveImage(filename):
   return url_for('static', filename=filename)

@app.route('/test2')
def test2():
   return render("landingpage.html",page_vars={},loginpath="/authenticate")

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

@app.route('/authenticate', methods=['GET','POST'])
def landingpage():
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

      if uamsecret:
         toHash = hexchal+uamsecret
      else:
         toHash = hexchal
      
      md5hash = hashlib.md5(toHash)
      newchal = md5hash.hexdigest()

      #url details dictionary
      lurldet =  {'uamip':request_data['uamip'],
                  'uamport':request_data['uamport'],
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
         print "generating chap response"
         print "password",request_data['password']
         print "newchal",newchal

         response = hashlib.md5(request_data['password']+newchal).hexdigest()
         logonUrl += "&response="+urllib.quote_plus(response)

      logonUrl += "&userurl="+urllib.quote_plus(request_data['userurl']);
      print "LoginURL:",logonUrl
      return redirect(logonUrl)

   #another part of the script
   result = 0
   if "res" not in request_data: pass
   elif request_data['res'] == "success":
      result = 1
   elif request_data['res'] == "failed":
      result = 2
   elif request_data['res'] == "logoff":
      result = 3
   elif request_data['res'] == "already":
      result = 4
   elif request_data['res'] == "notyet":
      result = 5
   elif request_data['res'] == "wispr":
      result = 6
   elif request_data['res'] == "popup1":
      result = 11
   elif request_data['res'] == "popup2":
      result = 12
   elif request_data['res'] == "popup3":
      result = 13

   if app.debug: print "Result:",result

   if result == 0:
      return error("WiFi Nation Login Failed","Login must be performed through CoovaChilli daemon.")

   if result == 6:
      pass

   if result == 2:
      if app.debug: print "WiFi Nation Login Failed!", request_data['reply']
      return render("landingpage.html",page_vars = {'error_msg':"WiFi Nation Login Failed"},loginpath="/authenticate")

   if result == 5:
      if app.debug: print "Not yet logged in"
      return render("landingpage.html",page_vars=request_data,loginpath="/authenticate")

   if result == 1:
      if app.debug: print "Logged in to WiFi Nation Success!"
      return render("simple.html",headline="Logged in to WiFi Nation!",mesg=request_data['reply'])

   if result == 4 or result == 12:
      logoutUrl = """<a href="http://%(uamip)s:%(uamport)s/logoff">Logout</a>"""%(request_data)
      if app.debug: print "Logout URL:",logoutUrl
      return render("simple.html",headline="Logged in to WiFi Nation!",mesg=logoutUrl)

   if result == 11:
      if app.debug: print "Logging in to WiFi Nation"
      return render("simple.html",headline="Logging in to WiFi Nation",mesg="Please wait...")

   if result == 13:
      if app.debug: print "Logged out from WiFi Nation"
      return render("simple.html",headline="Logged out from WiFi Nation",mesg="")

def redirect(redirect_url):
   if app.debug: print "Redirecting to",redirect_url
   return render("simple.html", redirect_url=redirect_url, mesg="Please Wait...",headline="Logging in to WiFi Nation")

def error(headline, mesg):
   if app.debug: print "Error:", headline, mesg
   return render("simple.html",headline=headline,mesg=mesg)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#http://localhost:5000/authenticate?res=notyet&uamip=192.168.182.1&uamport=3990&challenge=1f3590180f5ef93864dcfc0f5b17a15c&userurl=http%3a%2f%2fgeoip.ubuntu.com%2flookup&nasid=nas01&mac=E0-B9-A5-C6-59-1F
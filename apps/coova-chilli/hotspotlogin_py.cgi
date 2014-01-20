#!/usr/bin/env python
#@author Ivan Dominic Baguio
#made for WifiNation
#python implementation for hotspotlogin.cgi

uamsecret = "uamsecret"
login_path = "/cgi-bin/hotspotlogin.cgi"
DEBUG = 1

data = {}

def getdata(getvars):
   val = getvars.split("&")
   return val

def error(title, msg):
   #generate page with error

def redirect():
   pass

def main():
   if data['res'] == "wispr" && data['username']:
      hexchal = data["challenge"].decode("hex")
      if uamsecret:
         newchal = 
import MySQLdb

def getdb():
   return MySQLdb.connect(host="localhost", # your host, usually localhost
                  user="root", # your username
                   passwd="root", # your password
                   db="radius") # name of the data base

#adds new user to the radcheck table
def addUser(username,password="wifination"):
   db = getdb()
   sql = "INSERT INTO radcheck (username, attribute, op, value) VALUES \
   ('%s', 'Cleartext-Password', ':=', '%s');"%(username,password)

   cur = db.cursor()
   try:
      cur.execute(sql)
      db.commit()
      print "ok"
      return True
   except Exception, e:
      db.rollback()
      print "failed"
   finally:
      db.close()

#check if a username already exists in radcheck
def userExists(username):
   db = getdb()
   sql = "SELECT COUNT(*) from radcheck WHERE username = '%s'"%(username)
   cur = db.cursor()
   try:
      cur.execute(sql)
      if cur.fetchone()[0] > 0:
         return True
      return False
   except:
      print "Failed to query"

def addUserInfo(username, info):
   db = getdb()
   cur = db.cursor()

   def insertIt(key, val):
      try:
         sql = "INSERT INTO userdetails (username, attribute, value) VALUES \
            ('%s', '%s', '%s')"%(username, key, val)
         cur.execute(sql)
         db.commit()
      except:
         db.rollback()

   if not userExists(username):
      addUser(username)
   
   for key in info:
      if type(info[key]) == str:
         insertIt(key, info[key])
      elif type(info[key]) == dict:
         sinfo = info[key]
         for skey in sinfo:
            if skey == 'id': continue
            insertIt(key, sinfo[skey])
      elif key == 'education':
         for sinfo in info[key]:
            insertIt('school:'+sinfo['type'],sinfo['school']['name'])

   db.close()
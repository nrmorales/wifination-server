import MySQLdb

def getdb():
   return MySQLdb.connect(host="localhost", # your host, usually localhost
                  user="root", # your username
                   passwd="root", # your password
                   db="radius") # name of the data base

#adds new user to the radcheck table
def addUser(username,password="wifination"):
   db = getdb()
   sql = "INSERT INTO users (username) VALUES ('%s');"%(username)

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

#check if a username already exists in users table
def userExists(username):
   db = getdb()
   sql = "SELECT COUNT(*) from users WHERE username = '%s'"%(username)
   cur = db.cursor()
   try:
      cur.execute(sql)
      if cur.fetchone()[0] > 0:
         return True
   except:
      print "Failed to query"
      return False
   finally:
      db.close()

#returns the user_id of a specific username
def getUserId(username):
   db = getdb()
   cur = db.cursor()

   sql = "SELECT user_id from users WHERE username = '%s'"%(username)
   try:
      cur.execute(sql)
      uid = int(cur.fetchone()[0])
      if uid: return uid
   except:
      print "Failed to query"
      return False
   finally:
      db.close()

def addUserInfo(username, info):
   user_id = getUserId(username)
   if not user_id: return False

   db = getdb()
   cur = db.cursor()
   print "adding",username
   print "info",info
   def insertIt(key, val):
      try:
         print "inserting",key,":",val
         sql = "INSERT INTO userdetails (user_id, attribute, value) VALUES \
            ('%s', '%s', '%s')"%(user_id, key, val)
         cur.execute(sql)
         db.commit()
      except:
         db.rollback()

   if not userExists(username): addUser(username)
   
   for key in info:
      if type(info[key]) in [str,unicode]:
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

#TODO: escape question to block sql injections
def addSurvey(question,options):
   def addOption(survey_id,option,cur):
      try:
         sql = "INSERT INTO survey_options (survey_id, value) VALUES (%d, '%s')"%(survey_id,option)
         cur.execute(sql)
         db.commit()
         return True
      except:
         return

   if len(question) > 140: return

   db = getdb()
   cur = db.cursor()

   try:
      #add question
      sql = "INSERT INTO survey_questions (question) VALUES ('%s')"%(question)
      survey_id = cur.execute(sql)
      db.commit()
      for opt in options:
         if addOption(survey_id,opt,cur):
            print "Adding option: ",opt,"OK"
         else:
            print "Adding option: ",opt,"FAIL"
      return True
   except:
      db.rollback()
      return
   finally:
      db.close()

#inserts user answer to the survey_answers table
def saveAnswer(username, survey_id, option_id):
   db = getdb()
   cur = db.cursor()

   user_id = getUserId(username)

   try:
      sql = "INSERT INTO survey_answers (user_id, survey_id, option_id) VALUES (%d,%d,%d)"%(user_id,survey_id,option_id)
      cur.execute(sql)
      db.commit()
      return True
   except:
      db.rollback()
      return
   finally:
      db.close()
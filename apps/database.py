import MySQLdb

def getdb():
   return MySQLdb.connect(host="localhost", # your host, usually localhost
                  user="root", # your username
                   passwd="root", # your password
                   db="radius") # name of the data base

#adds new user to the radcheck table
def addUser(username):
   print "Adding new User:",username
   sql = "INSERT INTO users (username) VALUES ('%s');"%(username)
   db = getdb()
   cur = db.cursor()
   try:
      cur.execute(sql)
      db.commit()
      print "addUser(): Success"
      return True
   except Exception, e:
      db.rollback()
      print "addUser(): Failed"

#check if a username already exists in users table
def userExists(username):
   print "Checking if",username,"exists"
   db = getdb()
   sql = "SELECT COUNT(*) from users WHERE username = '%s'"%(username)
   print "SQL:",sql
   cur = db.cursor()
   try:
      cur.execute(sql)
      if cur.fetchone()[0] > 0:
         return True
      
   except Exception, e:
      print "userExists(): Failed to query"
      print e
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
      row = cur.fetchone()
      print "USERID:>",row
      if row: return int(row[0])
   except Exception, e:
      print "getUserId(): Failed to query"
      print e
      return False
   finally:
      db.close()

def addUserInfo(username, info):
   def insertIt(key, val):
      try:
         print "inserting",key,":",val
         sql = "INSERT INTO userdetails (user_id, attribute, value) VALUES \
            (%d, '%s', '%s')"%(user_id, key, val)
         print "SQL:",sql
         cur.execute(sql)
         db.commit()
      except Exception,e:
         print "insertIt:",e
         db.rollback()

   print "Adding info for",username,"Info:",info
   
   db = getdb()
   cur = db.cursor()
   user_id = getUserId(username)
   if not user_id:
      addUser(username)
      user_id = getUserId(username)
      if not user_id: return

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
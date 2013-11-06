from flaskext.mysql import MySQL

@app.route('/newuser',methods=["POST"])
def newUser():
   mysql = MySQL()
   mysql.init_app(app)

   cursor = mysql.get_db().cursor()
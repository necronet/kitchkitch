# all the imports
import sys
import getopt
import sqlite3
import kitch_db 
from flask import Flask, g, render_template
from contextlib import closing
from users.views import app as user
from menus.views import  app as menu
from flask import _app_ctx_stack, request
from flask.ext.login import LoginManager

#class KitchFlask(Flask):
#	def make_response(self, rv):
#		return Flask.make_response(self,rv)
		
app = Flask(__name__)
app.config.from_object('default_settings')
app.register_blueprint(menu)
app.register_blueprint(user)

loginManager = LoginManager()

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('docs/index.html')

if __name__=='__main__':
	try:
		optlist,argsX	=getopt.getopt(sys.argv[1:],'h',["init-db","help"])
		#init_db()
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)

	initialize_db=False
	for o, a in optlist:
		if o == "--init-db":
			initialize_db=True
		if o == "--help" or o=='-h':
			print "help me!"

	if initialize_db : 
		print "Initializing database"
		kitch_db.init_db()

	kitch_db.init_app(app)

	app.run(debug=True)
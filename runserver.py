# all the imports
import sqlite3
import kitch_db 
from flask import Flask, g, render_template
from users.views import app as user, User
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

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
	user = User()
	user.id=100
	return user

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('docs/index.html')

if __name__=='__main__':


	app.run(debug=True)
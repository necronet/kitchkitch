# all the imports
from flask import Flask, render_template, abort,jsonify
from users.views import app as user, User
from menus.views import  app as menu
from flask import request
from flask.ext.login import LoginManager


#In case we need a custom flask class
#class KitchFlask(Flask):
#	def make_response(self, rv):
#		return Flask.make_response(self,rv)
		
app = Flask(__name__)
app.config.from_object('default_settings')
app.register_blueprint(menu)
app.register_blueprint(user)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

@app.before_request
def validate_request():
	#ignore items validation if login or logout

	if request.endpoint == 'user.login':
		return None

	if request.mimetype=='application/json' and (request.method == 'POST' or request.method=='PUT' ):
		#In case no body is sent in body for post
		if not (request.json and request.json.has_key('items') ) or not isinstance(request.json['items'], (list,tuple)):
			return abort(400)


@app.errorhandler(400)
def bad_request_handler(error):

	reason='Unknown'
	if not request.json:
		reason='Empty body is not allowed please submit the proper data'
	elif not request.json.has_key('items'):
		reason='Body content should include items array. For call %s' % request.url
	elif not isinstance(request.json['items'], (list,tuple)):
		reason='Items must be a json array. Enclose with brackets items:[{}]'

	return jsonify({'message':'Error has occurred, reason %s' % reason} ), 400

@login_manager.user_loader
def load_user(uid):
	return User.get(uid)


@app.route('/',methods=['GET','POST'])
def index():
	return render_template('docs/index.html')

if __name__=='__main__':
	app.run(debug=app.config['DEBUG'])
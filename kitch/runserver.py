# all the imports
from flask import Flask, render_template
from utils.exceptions import abort
from users.views import app as user, User
from menus.views import  app as menu
from flask import request, _request_ctx_stack
from flask.ext.login import LoginManager


class CustomLoginManager(LoginManager):
	def reload_user(self):
		if request.headers.has_key('Authorization'):
			ctx = _request_ctx_stack.top
			ctx.user = User.get(token=request.headers['Authorization'])
		else:	
			super(CustomLoginManager,self).reload_user()
	

app = Flask(__name__)
app.config.from_object('default_settings')
app.register_blueprint(menu)
app.register_blueprint(user)

login_manager = CustomLoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

@app.before_request
def validate_request():

	if request.endpoint == 'user.login':
		return None
	#Validate mime type to always be json
	if request.mimetype!='application/json' and request.method != 'GET':
		abort(415)

	if request.method in ('POST','PUT'):
		#In case no body is sent in body for post
		if not (request.json and request.json.has_key('items') ) or not isinstance(request.json['items'], (list,tuple)):
			bad_request_response()


def bad_request_response():
	
	if not request.json:
		reason='Empty body is not allowed please submit the proper data'
	elif not request.json.has_key('items'):
		reason='Body content should include items array. For call %s' % request.url
	elif not isinstance(request.json['items'], (list,tuple)):
		reason='Items must be a json array. Enclose with brackets items:[{}]'

	return abort(400,'Error has occurred, reason %s' % reason )

@login_manager.user_loader
def load_user(uid):
	return User.get(uid)

@login_manager.unauthorized_handler
def unauthorized_call():

	return abort(401,'Unauthorized call please provide the proper credentials' )

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('docs/index.html')

if __name__=='__main__':
	app.run(debug=app.config['DEBUG'])
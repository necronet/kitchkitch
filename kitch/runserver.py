# all the imports
from flask import Flask, render_template
from utils.exceptions import abort, bad_request_response
from users.views import app as user, get_user, check_user_permission
from menus.views import  app as menu
from orders.views import app as table
from flask import request, _request_ctx_stack
from flask.ext.login import LoginManager
from models import db
from flask import json
import decimal

class APIEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, decimal.Decimal):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

class CustomLoginManager(LoginManager):

    def reload_user(self):

        if request.headers.has_key('Authorization') and request.endpoint:
            ctx = _request_ctx_stack.top
            ctx.user = get_user(token=request.headers['Authorization'])
            if ctx.user:
                check_user_permission(ctx.user)
            else:
                ctx.user = self.anonymous_user()

        else:
            super(CustomLoginManager,self).reload_user()


app = Flask(__name__)

login_manager = CustomLoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

app.json_encoder = APIEncoder

db.init_app(app)
app.config.from_object('default_settings')
app.register_blueprint(menu)
app.register_blueprint(user)
app.register_blueprint(table)


@app.before_request
def validate_request():

    """
        Ensure that the request sent has the proper basic information to
        be handle by the endpoint. Otherwise it would be a waste of resources
        to proceed to following stages.
    """

    #Validate mime type to always be json
    if request.mimetype!='application/json' and request.method != 'GET':
        abort(415)


    if request.method in ('POST','PUT') and not request.json:
        #in case there is no json data
        bad_request_response()

@login_manager.user_loader
def load_user(uid):
    return get_user(uid)

@login_manager.unauthorized_handler
def unauthorized_call():
    return abort(401,'Unauthorized call please provide the proper credentials' )

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

if __name__=='__main__':
    if app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('kitch.log','a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] [%(funcName)s() from %(module)s]'))
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('kitch app starting up....')
    app.run(debug=app.config['DEBUG'])
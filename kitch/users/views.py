from flask import request, flash, render_template, redirect, url_for,Blueprint,make_response,jsonify
from flask.ext.login import login_user,UserMixin, login_required, logout_user
from kitch_db import db
from utils.entities import BaseService
import uuid

app = Blueprint('user',__name__,template_folder='templates')

"""
    Most likely the only RPC-style method. In order to simplify this call, 
    login/logout are specially created to keep this format.
"""

class User(UserMixin):
    """
        User represent a user in the system. It contains 
        Username, Password and active state.
    """
    def __init__(self,uid, username, password,active):
        self.id=uid
        self.username=username
        self.password=password
        self.active=active

    def is_active(self):
        return self.active

    @staticmethod
    def get(uid=None, token=None):
        
        if uid is not None :
            record=db.get("select * from users where uid=%s",uid,)
            return create_user_from_record(record)
        elif token is not None :
            record=db.get("select * from tokens where token=%s and active=1",token,)

            if record is not None:
                return User.get(record.uid)

class UserService(BaseService):
    pass

class LoginService(BaseService):
    def get(self):
        return render_template('login.html')

    def post(self):
        user=validate_user()
        if user:
            login_user(user)
            if request.json:
                token=generate_token(user)
                return make_response(jsonify({'message':'Logged successfully','token':token}))
            else:
                return redirect(request.args.get("next") or url_for("index"))

        return make_response(jsonify({}),401,{'Location':request.url})

    """
        Use this method to logout, it will remove(active=0) the Login from the
        database or logout the user from the session
    """
    def delete(self,uid):
        print 'data '+uid
        logout_user()
        #TODO: still need to inactivate the token
        return self.delete_response()

def generate_token(user):
    token =str(uuid.uuid1())
    db.execute("insert into tokens(uid,token) values(%s,%s)",user.id, token,)
    db.commit()
    return token

def validate_user():
    if request.json:
        (username,password)=request.json['username'],request.json['password'] 
    else:
        (username,password)=request.form['username'],request.form['password'] 

    record=db.get("select * from users where username=%s and password=%s",username,password,)

    return create_user_from_record(record)



def create_user_from_record(record):

    if record is None: return record

    user =User(record.uid,record.username,record.password,record.active)
    return user



'''
Register a MethodView class to hold the standard pattern

GET: /url/
GET, DELETE: /url/[id]
PUT,POST: /url/

'''
def register_api(view, endpoint, url, pk, pk_type='string'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
        view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST','PUT',])
    app.add_url_rule('%s<%s:%s>' %(url,pk_type,pk), view_func=view_func,
        methods=['GET', 'DELETE'])


register_api(LoginService, 'loginService','/login/','uid')



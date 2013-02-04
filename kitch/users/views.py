from flask import request, flash, render_template, redirect, url_for,Blueprint,make_response,jsonify
from flask.ext.login import login_user,UserMixin, login_required, logout_user
from kitch_db import db
from utils.entities import BaseService, register_api,encrypt_with_interaction
from utils.exceptions import abort
import uuid

app = Blueprint('user',__name__,template_folder='templates')

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
    def get(self,uid):
        super(UserService, self).get(uid,'show_user.html')
        items=[]
        if uid is None:
            rows = db.query("select uid,username,pincode from user where active=1 limit %s offset %s" ,self.limit, self.offset )
            for row in rows:
                items.append( dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,username=row.username,pincode=row.pincode) )

        return self.get_response(items)

class LoginService(BaseService):
    def get(self,uid):
        return make_response(jsonify({}),501)

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
        logout_user()

        db.execute_rowcount('update tokens set active=0 where token=%s', uid)
        db.commit()

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

    if not password or not username:
        abort(400, 'Password or user cannot be empty')

    record_user=db.get("select * from users where username=%s",username,)
    password_encrypt=record_user.password

    record=db.get("select iteraction,product,modified_on from meta_users where user_uid=%s",record_user.uid,)

    #Ignore iterate, salt, time will not be use this time we just need the encrypted password
    password,_,_,_=encrypt_with_interaction(password,random_salt=record.product,iterate=record.iteraction,t=record.modified_on)

    if  password==password_encrypt:
        return create_user_from_record(record_user)

def create_user_from_record(record):

    if record is None: return record

    user =User(record.uid,record.username,record.password,record.active)
    return user

register_api(app,LoginService, 'loginService','/login/','uid')



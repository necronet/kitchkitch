from flask import request, redirect, url_for,Blueprint,make_response,jsonify
from flask.ext.login import login_user,logout_user,login_required
from kitch_db import db
from utils.entities import BaseService, register_api,encrypt_with_interaction
from utils.exceptions import abort
from models import User, MetaUser, Token, db as db2
import sqlalchemy
import uuid

app = Blueprint('user',__name__,template_folder='templates')


def get_user(uid=None, token=None):
        
    if uid is not None :
        record=db.get("select * from users where uid=%s",uid,)
        return create_user_from_record(record)
    elif token is not None :
        record=db.get("select * from tokens where token=%s and active=1",token,)

        if record is not None:
            return get_user(record.user_uid)

class UserService(BaseService):
    """
        Retrieve a User information, this can be useful for displaying in profile.
        Note this method will retrieve your profile along with the profile 
        that you are allow to see.
    """
    @login_required
    def get(self,uid):
        super(UserService, self).get(uid,'show_user.html')
        items=[]
        if uid is None:

            rows = User.query.filter_by(active=1).limit(self.limit).offset(self.offset).all()
            for row in rows:
                items.append( dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,username=row.username,pincode=row.pincode) )
        else:
            row = User.query.filter_by(active=1, uid=uid).limit(self.limit).offset(self.offset).first()#db.get("select uid,username,pincode from users where active=1 and uid=%s" , uid )
            
            items=dict(href='%s'%(request.base_url,),uid=row.uid,username=row.username,pincode=row.pincode) 
        
        return self.get_response(items)

    """
        Create a new User in the system. The structure that need to be provided is the following:

        {
            username:username,
            password:password,
            pincode:pincode
        }
        Then the method will ensure to hashed the password properly
    """
    @login_required
    def post(self):
        json = request.json
        uid =str(uuid.uuid1())
        try:
            
            password,iterate,t,random_salt=encrypt_with_interaction(json['password'])
            user = User(uid,json['username'],password,json['pincode'])
            meta_user = MetaUser(uid, iterate, random_salt,t)
            db2.session.add(user)
            db2.session.add(meta_user)
            db2.session.commit()
            return self.post_response()
        except sqlalchemy.exc.IntegrityError as e:
            abort(409, 'This username already exist. %s' % e.message)

    '''
    Update a user record. The method will ensure that to update the password if changed and re-hashed again.
    Aditionally all tokens related to thes User will be inactivated if pasword changed.
    '''
    @login_required
    def put(self):
        
        json = request.json
        if json['uid']:
            
            record=MetaUser.query.filter_by(user_uid = json['uid']).first()
            user = User.query.filter_by( uid = json['uid'], active=1).first()

            #Ignore iterate, salt, time will not be use this time we just need the encrypted password
            new_password,_,_,_=encrypt_with_interaction( json['password'],
                                                         random_salt=record.product,
                                                         iterate=record.iteraction,
                                                         t=record.modified_on )
            

            
            current_password = user.password
            

            if current_password != new_password:
                #Create a new salted password
                new_password,iterate,t,random_salt = encrypt_with_interaction(json['password'])
                #Now inactive all token related to the user so we can asked him to login again
                Token.query.filter_by(user_uid = json['uid']).update( dict ( active = 0 ))

                #Overwrite the meta user information of the password
                meta_user = MetaUser.query.filter_by( user_uid = json['uid'] )
                meta_user.iteraction = iterate
                meta_user.product = random_salt
                meta_user.modified_on = t
                user.password = new_password
                
                #db.execute('update tokens set active=0 where user_uid=%s',  json['uid'])
                
            
            user.pincode = json['pincode']
            

            #db.execute('update users set pincode=%s, password=%s where uid=%s',  json['pincode'],new_password, json['uid'])
            
            
            #db.execute('update meta_users set iteraction=%s, product=%s, modified_on=%s where user_uid=%s ', iterate,random_salt,t,json['uid'])
            
            db2.session.commit()
            #db.commit()

        return self.put_response()

    @login_required
    def delete(self, uid):
        user = User.query.filter_by( uid = uid).first()
        user.active = 0
        db2.session.commit()
        return self.delete_response()

        

class LoginService(BaseService):
    def get(self,uid):
        return make_response(jsonify({}),501)

    def put(self):
        return make_response(jsonify({}),501)

    """ To authenticate to the app, make a POST call to the Login with a JSON containing the username and password.
        This method will return a Authentication token that you can use to make authenticated calls.
    """
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
        To logout make a DELETE call to Login resources, it will remove(active=0) the curernt Login and logout 
        the user session.
    """
    def delete(self,uid):
        logout_user()

        db.execute_rowcount('update tokens set active=0 where token=%s', uid)
        db.commit()

        return self.delete_response()

def generate_token(user):
    token =str(uuid.uuid1())
    db.execute("insert into tokens(user_uid,token) values(%s,%s)",user.uid, token,)
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
register_api(app,UserService, 'userService','/user/','uid')



from flask import request, redirect, url_for, Blueprint, make_response, jsonify, render_template
from flask.ext.login import login_user,logout_user, login_required, current_user
from utils.entities import BaseService, register_api,encrypt_with_interaction
from utils.exceptions import abort
from models import User, GroupResourcePermission, Group, UserGroup, MetaUser, Token, Permission, Resource, db
import uuid



def get_user(uid=None, token=None):        
    if uid is not None :
        return create_user_from_record( User.query.filter_by( uid = uid, active=1 ).first() )
    elif token is not None :
        token = Token.query.filter_by( active = 1, token = token ).first()        
        if token is not None:
            return get_user(token.user_uid)

class UserService(BaseService):
    """
        Retrieve a User information, this can be useful for displaying in profile.
        Note this method will retrieve your profile along with the profile 
        that you are allow to see.
    """
    schema_table = User

    @login_required
    def get(self,uid):
        query_result = super(UserService, self).get(uid,'show_user.html')

        if type(query_result) == list:
            return self.get_response( [ row.as_dict() for row in query_result ] )
        else:
            return self.get_response( query_result.as_dict() )
        

    """
        Create a new User in the system. The structure that need to be provided is the following:

        {
            username:username,
            password:password,
            pincode:pincode
        }
        Then the method will ensure to hashed the password properly
    """
    def object_from_json(self,uid,json):
        password,iterate,t,random_salt=encrypt_with_interaction(json['password'])
        user = User(uid,json['username'],password,json['pincode'])
        meta_user = MetaUser(uid, iterate, random_salt,t)
        return [user,meta_user]


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
            
            user.pincode = json['pincode']
             
            db.session.commit()
            

        return self.put_response()

class LoginService(BaseService):
    schema_table = Token
    def get(self,uid):

        if not current_user.is_anonymous():
            return redirect(url_for("index"))

        #TODO: smelli this kind of call should be modularize
        best_match = request.accept_mimetypes.best_match(['application/json','text/html']) 
        if best_match == 'text/html':
            return render_template('login.html')
        else:
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
        elif request.json:
                return make_response(jsonify({}),401,{'Location':request.url})

        #When user is not logged and it was not a json requqest we render template as GET does.
        return self.get(None)
        

    """
        To logout make a DELETE call to Login resources, it will remove(active=0) the curernt Login and logout 
        the user session.
    """
    def delete(self,uid):
        logout_user()
        Token.query.filter_by(token = uid).update( dict( active = 0) )
        db.session.commit()
        return self.delete_response()

def generate_token(user):
    token =str(uuid.uuid1())
    token = Token (user.uid, token )
    db.session.add(token)
    db.session.commit()
    return token.token

def validate_user():
    if request.json:
        (username,password)=request.json['username'],request.json['password'] 
    else:
        (username,password)=request.form['username'],request.form['password']

    if not password or not username:
        abort(400, 'Password or user cannot be empty')


    user = User.query.filter_by( username = username ).first()

    if not user:
        return user

    meta_user = MetaUser.query.filter_by( user_uid = user.uid ).first()
    #record=db.get("select iteraction,product,modified_on from meta_users where user_uid=%s",record_user.uid,)

    #Ignore iterate, salt, time will not be use this time we just need the encrypted password
    password,_,_,_=encrypt_with_interaction(password,random_salt=meta_user.product,iterate=meta_user.iteraction,t=meta_user.modified_on)

    if  password==user.password:
        return create_user_from_record(user)

def create_user_from_record(record):

    if record is None: return record

    user =User(record.uid,record.username,record.password,record.active)
    return user



def check_user_permission(user):
    #Fetch to see wether the user has the permission in one of the groups where he is.
    resource = request.endpoint.split('.')[0]
    permission = request.method

    result = GroupResourcePermission.query.join(Group,Permission, Resource)\
            .filter(Permission.name == permission, Resource.name==resource).\
                join(UserGroup).join(User).filter(User.uid==user.uid).all()

    if not result:
        abort(403,"Not authorized to access this resource")

app = Blueprint('user',__name__,template_folder='templates')
register_api(app,LoginService, 'loginService','/login/','uid')
register_api(app,UserService, 'userService','/user/','uid')


#Logout method 
@app.route('/logout/')
@login_required
def logout():
    LoginService().delete(current_user.uid)

    return redirect(url_for('user.loginService'))

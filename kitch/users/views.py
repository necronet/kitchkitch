from flask import request, flash, render_template, redirect, url_for,Blueprint,make_response,jsonify
from flask.ext.login import login_user,UserMixin, login_required, logout_user
from kitch_db import db
import uuid

app = Blueprint('user',__name__,template_folder='templates')


class User(UserMixin):
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


def create_user_from_record(record):
    
    user =User(record.uid,record.username,record.password,record.active)
    return user

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user=validate_user()
        if(user):
            login_user(user)
            if request.json:
                token=generate_token(user)
                return make_response(jsonify({'message':'Logged successfully','token':token}))
            else:
                flash('You were logged in')
                return redirect(request.args.get("next") or url_for("index"))
        else:
            return make_response(jsonify({}),401,{'Location':request.url})
    
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('menus.list'))

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
    
    if record is not None:
        return create_user_from_record(record)
    return record
    

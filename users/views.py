from flask import request, flash, render_template, redirect, url_for
from flask import Blueprint
from flask.ext.login import login_user,UserMixin, login_required, logout_user
from kitch_db import db

app = Blueprint('user',__name__,template_folder='templates')

class User(UserMixin):
    pass

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user=validate_user()
        if(user):
            login_user(user)
            flash('You were logged in')
            return redirect(request.args.get("next") or url_for("index"))
        
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('menus.list'))


def validate_user():

    if request.json:
        (username,password)=request.json['username'],request.json['password'] 
    else:
        (username,password)=request.form['username'],request.form['password'] 


    record=db.execute('select * from users where username=? and password=?',[username,password]).fetchone()
    return record
    

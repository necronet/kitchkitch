from flask import request, session, flash, render_template, current_app, redirect, url_for
from flask import Blueprint
from flask.ext.login import login_user,UserMixin, login_required, logout_user
from kitch_db import db

app = Blueprint('user',__name__,template_folder='templates')

class User(UserMixin):
    pass

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user=validate_user(request.form['username'],request.form['password'] )
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


def validate_user(username, password):
    record=db.execute('select * from users where username=? and password=?',[username,password]).fetchdone()
    print record
    

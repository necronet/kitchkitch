from flask import request, session, flash, render_template, current_app, redirect, url_for
from flask import Blueprint
from flask.ext.login import login_user

app = Blueprint('user',__name__,template_folder='templates')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        if(request.form['username'] != current_app.config['USERNAME'] and request.form['password'] != current_app.config['PASSWORD']):
            login_user(user)
            flash('You were logged in')
            return redirect(request.args.get("next") or url_for("index"))
        
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('menus.list'))
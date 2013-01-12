from flask import request, session, flash, render_template, current_app, redirect, url_for
from flask import Blueprint
from flask.ext.login import login_user,UserMixin, login_required, logout_user

app = Blueprint('user',__name__,template_folder='templates')

class User(UserMixin):
    pass

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        if(request.form['username'] == current_app.config['USERNAME'] and request.form['password'] == current_app.config['PASSWORD']):
            user = User ()
            user.id=100

            login_user(user)
            flash('You were logged in')
            return redirect(request.args.get("next") or url_for("index"))
        
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('menus.list'))
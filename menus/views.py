from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask import Blueprint
from kitch_db import db

app = Blueprint('menus',__name__,template_folder='templates')


@app.route('/menu/',methods=['GET'])
def list():
    cur = db.execute('select title from menus')
    menus = [dict(title=row[0]) for row in cur.fetchall()]
    return render_template('show_menus.html', menus=menus)
    

@app.route('/menu/',methods=['POST'])
def update():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into menus(title) values(?) ', [request.form['title']])
    g.db.commit()
    flash('New entry was succesfully posted')

    return redirect(url_for('menus.list'))

@app.route('/menu/',methods=['DELETE'])
def delete():
    return 'DElete Menu'
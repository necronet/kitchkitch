from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask import Blueprint,jsonify, make_response, Response
from kitch_db import db


app = Blueprint('menus',__name__,template_folder='templates')


@app.route('/menus/',methods=['GET'])
def list():
    
    json_mime = request.accept_mimetypes.best_match(['application/json','text/html'])
    
    cur = db.execute('select title from menus')
    menus = [dict(title=row[0]) for row in cur.fetchall()]

    if json_mime=='application/json':
        return jsonify(items=menus)
    elif json_mime=='text/html':
        return render_template('show_menus.html', menus=menus)
    

@app.route('/menus/',methods=['POST'])
def update():
    
    if request.json:
        print 'comes with a json body'

    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into menus(title) values(?) ', [request.form['title']])
    g.db.commit()
    flash('New entry was succesfully posted')

    return redirect(url_for('menus.list'))

@app.route('/menus/<string:id>',methods=['DELETE'])
def delete(id):
    rowcount = db.executemany('delete from menus where id=?', id).rowcount
    
    if rowcount != 0:
        return Response(status= 200)
    
    response = { 'message':'Delete succesfully'}
    return make_response(jsonify(response), 202)

    
    

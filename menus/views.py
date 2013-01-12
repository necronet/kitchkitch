from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask import Blueprint,jsonify, make_response, Response
from kitch_db import db
import json
from flask.ext.login import login_required

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
#@login_required
def post():
    
    for json_object in request.json['items']:
        db.execute('insert into menus(title) values(?) ', [json_object['title']])
        response=make_response(jsonify({'message':'Inserted succesfully'}),201,{'location':request.url})

    db.commit()

    return response

@app.route('/menus/',methods=['PUT'])
def put():
    for json_object in request.json['items']:
        if json_object.has_key('id'):
            db.execute('update menus set title=? where id=?',  [json_object['title'],json_object['id']])
            
    db.commit()

    return make_response(jsonify({'message':'Succesfully updated'}))

@app.route('/menus/<string:id>',methods=['DELETE'])
@login_required
def delete(id):
    rowcount = db.executemany('delete from menus where id=?', id).rowcount
    
    if rowcount != 0:
        return Response(status= 200)
    
    response = { 'message':'Delete succesfully'}
    return make_response(jsonify(response), 202)

    
    

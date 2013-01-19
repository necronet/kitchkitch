import uuid
from flask import request, render_template,Blueprint,jsonify, make_response, Response
from flask.views import MethodView
from kitch_db import db
from flask.ext.login import login_required

class MenuService(MethodView):
    
    #@login_required
    def get(self, menu_id):
    
        json_mime = request.accept_mimetypes.best_match(['application/json','text/html'])
        
        cur = db.execute('select uid,title from menus')
        menus = [dict(uid=row[0],title=row[1]) for row in cur.fetchall()]

        if json_mime=='application/json':
            return jsonify(items=menus)
        elif json_mime=='text/html':
            return render_template('show_menus.html', menus=menus)

    
    #@login_required
    def post(self):

        for json_object in request.json['items']:
            uid =str(uuid.uuid1())
            db.execute('insert into menus(uid,title) values(?,?) ', [uid,json_object['title']])
            response=make_response(jsonify({'message':'Inserted succesfully'}),201,{'Location':request.url})

        db.commit()

        return response

    
    def put(self):
        for json_object in request.json['items']:
            if json_object.has_key('id'):
                db.execute('update menus set title=? where id=?',  [json_object['title'],json_object['id']])
                
        db.commit()

        return make_response(jsonify({'message':'Succesfully updated'}))


    def delete(self, menu_id):

        rowcount = db.execute('delete from menus where uid=?', (menu_id,)).rowcount
        db.commit()
        print rowcount
        if rowcount == 0:
            return Response(status= 200)
        
        response = { 'message':'Delete succesfully'}
        return make_response(jsonify(response), 202)



app = Blueprint('menus',__name__,template_folder='templates')

user_view = MenuService.as_view('menu_service')
app.add_url_rule('/menus/', defaults={'menu_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/menus/', view_func=user_view, methods=['POST','PUT',])
app.add_url_rule('/menus/<string:menu_id>', view_func=user_view,
                 methods=['GET', 'DELETE'])
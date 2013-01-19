import uuid
from flask import request, render_template,Blueprint,jsonify, make_response, Response
from utils.exceptions import abort
from flask.views import MethodView
from kitch_db import db


class MenuService(MethodView):
    
    #@login_required
    def get(self, menu_uid):
        
        json_mime = request.accept_mimetypes.best_match(['application/json','text/html'])
        
        cur = db.execute('select uid,title from menus where active=1')
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


    def delete(self, menu_uid):

        rowcount = db.execute('update menus set active=0 where uid=?', (menu_uid,)).rowcount
        db.commit()
        
        if rowcount == 0:
            return Response(status= 200)
        
        response = { 'message':'Delete succesfully'}
        return make_response(jsonify(response), 202)

class MenuItemsService(MethodView):
    def get(self, item_uid):

        json_mime = request.accept_mimetypes.best_match(['application/json'])
        
        cur = db.execute('select uid,title,description,price from items where active=1')
        menus_items = [dict(uid=row[0],title=row[1],description=row[2],price=row[3]) for row in cur.fetchall()]
        
        if json_mime=='application/json':
            return jsonify(items=menus_items)
        
    def post(self):

        if request.args.get('menus_uid') is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to create items without a menu to be referenced')

        for json_object in request.json['items']:
            uid =str(uuid.uuid1())
            db.execute('insert into items(uid,title,description,price) values(?,?,?,?) ', [uid,json_object['title'],json_object['description'],json_object['price']])


            response=make_response(jsonify({'message':'Inserted succesfully'}),201,{'Location':request.url})

        db.commit()

        return response

    def put(self):
        return 'Success'
    def delete(self,item_uid):
        return 'Success'



app = Blueprint('menus',__name__,template_folder='templates')



'''
Register a MethodView class to hold the standard pattern

GET: /url/ 
GET, DELETE: /url/[id] 
PUT,POST: /url/

'''
def register_api(view, endpoint, url, pk, pk_type='string'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST','PUT',])
    app.add_url_rule('%s<%s:%s>' %(url,pk_type,pk), view_func=view_func,
                     methods=['GET', 'DELETE'])



register_api(MenuService, 'menuService','/menus/','menu_uid')
register_api(MenuItemsService, 'menuItemService','/menuItems/','item_uid')



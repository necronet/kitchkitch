import uuid
from utils.entities import KitchObject, BaseService
from flask import request, render_template,Blueprint,jsonify, make_response, Response, url_for
from utils.exceptions import abort
from kitch_db import db
from flask.ext.login import login_required

'''
    Represent menus with associated their dishes as a collection of items. It consist on standars
    REST calls GET for listing, POST for creating, PUT for modifying and DELETE to mark as remove.

'''
class MenuService(BaseService):
    
    @login_required
    def get(self, uid):
        super(MenuService, self).get(uid)
        json_mime = request.accept_mimetypes.best_match(['application/json','text/html'])
        
        if uid is None:

            rows = db.query("select uid,title from menus where active=1 limit %s offset %s" ,self.limit, self.offset )
            items=[]
            for row in rows:
                menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_method='GET',_external=True),row.uid,))
                items.append( dict(href='%s%s'%(request.url,row.uid),uid=row.uid,title=row.title,items=menu_items) )

            response=jsonify(items=items)
        else:

            result = db.get("select uid,title from menus where uid=%s and active=1 limit %s offset %s" ,uid,self.limit, self.offset) 

            items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_method='GET',_external=True),result.uid,) )

            item = dict(href="%s" % (request.url,),uid=result.uid,title=result.title, items=items)

            response=jsonify(item)

        if json_mime=='application/json':
            return response
        elif json_mime=='text/html':
            return render_template('show_menus.html', menus=items)

    
    @login_required
    def post(self):
        for json_object in request.json['items']:
            menu= KitchObject(json_object)
            uid =str(uuid.uuid1())
            #TODO: add location to each item
            db.execute('insert into menus(uid,title) values(%s,%s) ', uid,menu.title)
            response=make_response(jsonify({'message':'Inserted succesfully'}),201,{'Location':request.url})
            db.commit()
        

        return response

    @login_required
    def put(self):
        for json_object in request.json['items']:
            menu= KitchObject(json_object)
            if json_object.has_key('uid'):
                db.execute('update menus set title=%s where uid=%s',  menu.title,menu.uid)
                db.commit()

        return make_response(jsonify({'message':'Succesfully updated'}))

    @login_required
    def delete(self, uid):

        rowcount = db.execute_rowcount('update menus set active=0 where uid=%s', uid)
        db.commit()
        if rowcount == 0:
            return Response(status= 200)
        
        response = { 'message':'Delete succesfully'}
        return make_response(jsonify(response), 202)

class MenuItemsService(BaseService):
    def get(self, uid):
        super(MenuItemsService, self).get(uid)
        menus_uid=request.args.get('menus_uid')
        
        json_mime = request.accept_mimetypes.best_match(['application/json'])

        if uid is not None:
            result = db.get('select uid,title,description,price from items where uid=%s and active=1 limit %s offset %s',uid,self.limit, self.offset)

            item = dict(href='%s'%(request.url), uid=result.uid,title=result.title,description=result.description,price=str(result.price))
            return jsonify(item)
        
        if menus_uid is None:
            result = db.query("select uid,title,description,price from items where active=1 limit %s offset %s", self.limit, self.offset)
        else:
            result = db.query("select uid,title,description,price from items i inner join menus_items mi on mi.items_uid=i.uid where mi.active=1 and mi.menus_uid=%s limit %s offset %s" ,menus_uid,self.limit, self.offset)
        menus_items = [dict(href='%s%s'%(request.url,row.uid),uid=row.uid,title=row.title,description=row.description,price=str(row.price)) for row in result]
        
        if json_mime=='application/json':
            return jsonify(items=menus_items)
        
    def post(self):
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to create items without a menu to be referenced')


        for json_object in request.json['items']:
            menu_items= KitchObject(json_object)
            uid =str(uuid.uuid1())

            db.execute('insert into items(uid,title,description,price) values(%s,%s,%s,%s) ', uid,menu_items.title,menu_items.description,menu_items.price)
            db.execute('insert into menus_items(menus_uid,items_uid) values(%s,%s) ', menus_uid,uid)
            db.commit()
        
        response=make_response(jsonify({'message':'Inserted succesfully'}),201,{'Location':request.url})

        

        return response

    def put(self):

        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to update items without a menu to be referenced')

        for json_object in request.json['items']:            

            menu_items= KitchObject(json_object)
            db.execute("update items set title=%s, description=%s, price=%s where uid=%s",  menu_items.title,menu_items.description,menu_items.price,menu_items.uid)
            db.execute("update menus_items set menus_uid=%s where items_uid=%s",menus_uid,menu_items.uid)
            db.commit()

        return make_response(jsonify({'message':'Succesfully updated'}))
    def delete(self,uid):

        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to delete items without a menu to be referenced')
        
        rowcount = db.execute_rowcount('update menus_items set active=0 where menus_uid=%s and items_uid=%s', menus_uid,uid)
        db.commit()
        
        
        if rowcount == 0:
            return Response(status= 200)
        
        response = { 'message':'Delete succesfully'}
        return make_response(jsonify(response), 202)

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



register_api(MenuService, 'menuService','/menus/','uid')
register_api(MenuItemsService, 'menuItemService','/menuItems/','uid')



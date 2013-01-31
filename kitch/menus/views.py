import uuid
from utils.entities import KitchObject, BaseService
from flask import request, Blueprint,url_for
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
        super(MenuService, self).get(uid,'show_menu.html')

        menu_items=[]
        if uid is None:

            rows = db.query("select uid,title from menus where active=1 limit %s offset %s" ,self.limit, self.offset )
            items=[]

            for row in rows:

                if self.expand is not None:
                    for argument in self.expand_arguments():
                        if argument == 'items':
                            menu_items = self.fetch_items(row.uid)

                if not menu_items:
                    menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_method='GET',_external=True),row.uid,))

                items.append( dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,title=row.title,items=menu_items) )
        else:
            result = db.get("select uid,title from menus where uid=%s and active=1 limit %s offset %s" ,uid,self.limit, self.offset)

            if self.expand is not None:
                for argument in self.expand_arguments():

                    if argument == 'items':
                        menu_items= self.fetch_items(uid)

            if not menu_items:
                menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_method='GET',_external=True),result.uid,) )

            items = dict(href="%s" % (request.base_url,),uid=result.uid,title=result.title, items=menu_items)

        return self.get_response(items)
       

    def fetch_items(self,uid):
        #print "select uid,title,description,price from items i inner join menus_items mi on mi.items_uid=i.uid where mi.active=1 and mi.menus_uid=%s" % uid
        result= db.query("select uid,title,description,price from items i inner join menus_items mi on mi.items_uid=i.uid where mi.active=1 and mi.menus_uid=%s" ,uid)
        menu_items= [dict(href='%s%s'%(url_for('.menuItemService',_method='GET',_external=True),item.uid),uid=item.uid,title=item.title,description=item.description,price=str(item.price)) for item in result]
        #print uid
        return menu_items
    
    @login_required
    def post(self):
        for json_object in request.json['items']:
            menu= KitchObject(json_object)
            uid =str(uuid.uuid1())
            #TODO: add location to each item
            db.execute('insert into menus(uid,title) values(%s,%s) ', uid,menu.title)
            
            db.commit()
        
        return self.post_response()

    @login_required
    def put(self):
        for json_object in request.json['items']:
            menu= KitchObject(json_object)
            if json_object.has_key('uid'):
                db.execute('update menus set title=%s where uid=%s',  menu.title,menu.uid)
                db.commit()

        return self.put_response()

    @login_required
    def delete(self, uid):
        db.execute_rowcount('update menus set active=0 where uid=%s', uid)
        db.commit()
        return self.delete_response()

class MenuItemsService(BaseService):
    def get(self, uid):
        super(MenuItemsService, self).get(uid)
        menus_uid=request.args.get('menus_uid')

        if uid is not None:
            result = db.get('select uid,title,description,price from items where uid=%s and active=1 limit %s offset %s',uid,self.limit, self.offset)
            items = dict(href='%s%s'%(request.base_url,uid), uid=result.uid,title=result.title,description=result.description,price=str(result.price))
            return self.get_response(items)

        if menus_uid is None:
            result = db.query("select uid,title,description,price from items where active=1 limit %s offset %s", self.limit, self.offset)
        else:
            result = db.query("select uid,title,description,price from items i inner join menus_items mi on mi.items_uid=i.uid where mi.active=1 and mi.menus_uid=%s limit %s offset %s" ,menus_uid,self.limit, self.offset)
        
        items = [dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,title=row.title,description=row.description,price=str(row.price)) for row in result]
        
        return self.get_response(items)
        
        
    def post(self):
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to create items without a menu to be referenced')

        
        for json_object in request.json['items']:
            menu_items=KitchObject(json_object)            
            uid =str(uuid.uuid1())

            db.execute('insert into items(uid,title,description,price) values(%s,%s,%s,%s) ', uid,menu_items.title,menu_items.description,menu_items.price)
            db.execute('insert into menus_items(menus_uid,items_uid) values(%s,%s) ', menus_uid,uid)
            db.commit()        
        
        return self.post_response()

    def put(self):

        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to update items without a menu to be referenced')

        for json_object in request.json['items']:            

            menu_items= KitchObject(json_object)
            db.execute("update items set title=%s, description=%s, price=%s where uid=%s",  menu_items.title,menu_items.description,menu_items.price,menu_items.uid)
            db.execute("update menus_items set menus_uid=%s where items_uid=%s",menus_uid,menu_items.uid)
            db.commit()

        return self.put_response()
    def delete(self,uid):

        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to delete items without a menu to be referenced')
        
        db.execute_rowcount('update menus_items set active=0 where menus_uid=%s and items_uid=%s', menus_uid,uid)
        db.commit()
        
        
        return self.delete_response()

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



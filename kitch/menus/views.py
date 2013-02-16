import uuid
from utils.entities import BaseService, register_api
from flask import request, Blueprint,url_for
from utils.exceptions import abort
from flask.ext.login import login_required
from models import Menu, Item, MenuItem, db

class MenuService(BaseService):
    """
    Represent menus with associated their dishes as a collection of items.
    It consist on standars REST calls GET for listing, POST for creating,
    PUT for modifying and DELETE to mark as remove.
    """
    schema_table=Menu

    @login_required
    def get(self, uid):
        super(MenuService, self).get(uid,'show_menu.html')
        menu_items=[]
        if uid is None:
            
            rows = Menu.query.filter_by(active=1).limit(self.limit).offset(self.offset).all()

            items=[]
            for row in rows:

                if self.expand is not None:
                    for argument in self.expand_arguments():
                        if argument == 'items':
                            menu_items = self.fetch_items(row.uid)

                if not menu_items:
                    menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_external=True),row.uid,))

                items.append( dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,title=row.title,items=menu_items) )
                
        else:
            result = Menu.query.filter_by(active=1, uid=uid).limit(self.limit).offset(self.offset).first()
            
            if self.expand is not None:
                for argument in self.expand_arguments():

                    if argument == 'items':
                        menu_items= self.fetch_items(uid)

            if not menu_items:
                menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_external=True),result.uid,) )

            items = dict(href="%s" % (request.base_url,),uid=result.uid,title=result.title, items=menu_items)

        return self.get_response(items)
    
    def update_object(self,json):
        menu = Menu.query.filter_by(active=1, uid=json['uid']).first()
        menu.title=json['title']

    def fetch_items(self,uid):
        result= Item.query.join(Item.menuItems).filter(MenuItem.active==1, MenuItem.menus_uid==uid).all()
        menu_items= [dict(href='%s%s'%(url_for('.menuItemService',_method='GET',_external=True),item.uid),uid=item.uid,title=item.title,description=item.description,price=str(item.price)) for item in result]
        return menu_items
    
    def object_from_json(self,uid,json):
        return Menu(uid,json['title'])


class MenuItemsService(BaseService):
    schema_table='items'
    @login_required
    def get(self, uid):
        super(MenuItemsService, self).get(uid)
        menus_uid=request.args.get('menus_uid')

        if uid is not None:
            result = Item.query.filter_by(active=1, uid=uid).limit(self.limit).offset(self.offset).first()
            items = dict(href='%s%s'%(request.base_url,uid), uid=result.uid,title=result.title,description=result.description,price=str(result.price))
            return self.get_response(items)

        if menus_uid is None:
            result = Item.query.filter_by(active=1).limit(self.limit).offset(self.offset).all()
        else:
            result = Item.query.join(Item.menuItems).filter(MenuItem.active==1, MenuItem.menus_uid==menus_uid).limit(self.limit).offset(self.offset).all()
        
        items = [dict(href='%s%s'%(request.base_url,row.uid),uid=row.uid,title=row.title,description=row.description,price=str(row.price)) for row in result]
        
        return self.get_response(items)
        
    @login_required    
    def post(self):
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to create items without a menu to be referenced')

        json=request.json
        uid =str(uuid.uuid1())
        item = Item(uid,json['title'],json['description'],json['price'])
        menu_item = MenuItem(menus_uid,uid)
        db.session.add(item)
        db.session.add(menu_item)
        db.session.commit()
        
        return self.post_response()

    @login_required
    def put(self):

        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to update items without a menu to be referenced')

        json=request.json
        item=Item.query.filter_by(active=1, uid=json['uid']).first()
        item.title=json['title']
        item.description=json['description']
        item.price=json['price']
        
        menu_item=MenuItem.query.filter_by(active=1, items_uid=json['uid']).first()
        menu_item.menus_uid=menus_uid
        
        db.session.commit()

        return self.put_response()
    @login_required
    def delete(self,uid):
        
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to delete items without a menu to be referenced')

        menu_item = MenuItem.query.filter_by(active=1, items_uid=uid, menus_uid=menus_uid).first()
        menu_item.active = 0
        db.session.commit()

        return self.delete_response()

app = Blueprint('menus',__name__,template_folder='templates')


register_api(app,MenuService, 'menuService','/menus/','uid')
register_api(app,MenuItemsService, 'menuItemService','/menuItems/','uid')



from utils.entities import BaseService, register_api
from flask import request, Blueprint,url_for
from utils.exceptions import abort
from flask.ext.login import login_required
from models import Menu, Item, MenuItem

class MenuService(BaseService):
    """
    Represent menus with associated their dishes as a collection of items.
    It consist on standars REST calls GET for listing, POST for creating,
    PUT for modifying and DELETE to mark as remove.
    """
    schema_table=Menu

    @login_required
    def get(self, uid):
        query_result=super(MenuService, self).get(uid, 'show_menu.html')

        if type(query_result) == list:
            return self.get_response( [self.retrieve_object(row) for row in query_result] )
        else:
            return self.get_response(self.retrieve_object(query_result))

    def retrieve_object(self, row):
        item = row.as_dict()
                
        if 'items' in self.expand_arguments() :
            menu_items = self.fetch_items(row.uid)
        else:
            menu_items=dict(href='%s?menus_uid=%s' % ( url_for('.menuItemService',_external=True),row.uid,))
                
        item['items'] = menu_items

        return item
    
    def update_object(self,json):
        menu = Menu.query.filter_by(active=1, uid=json['uid']).first()
        menu.title=json['title']

    def fetch_items(self,uid):
        result= Item.query.join(Item.menuItems).filter(MenuItem.active==1, MenuItem.menus_uid==uid).all()
        menu_items= [dict(href='%s%s'%(url_for('.menuItemService',_method='GET',_external=True),item.uid),uid=item.uid,title=item.title,description=item.description,price=str(item.price)) for item in result]
        return menu_items
    
    def object_from_json(self,uid,json):
        return [Menu(uid,json['title'])]


class MenuItemsService(BaseService):
    schema_table = Item
    @login_required
    def get(self, uid):

        menus_uid=request.args.get('menus_uid')

        if menus_uid:
            query_result = super(MenuItemsService, self).get(join=Item.menuItems, active=1, menus_uid=menus_uid )
            return self.get_response( [row.as_dict() for row in query_result] )
        else:
            query_result = super(MenuItemsService, self).get(uid)

            if uid:
                result = query_result.as_dict()
            else:
                result = [ row.as_dict() for row in query_result ] 
            
            return self.get_response( result )


        
    def object_from_json(self,uid,json):
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to create items without a menu to be referenced')
        
        item = Item(uid,json['title'],json['description'],json['price'])
        menu_item = MenuItem(menus_uid,uid)
        
        return [item,menu_item]

    def update_object(self,json):
        menus_uid=request.args.get('menus_uid')

        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to update items without a menu to be referenced')

        item=Item.query.filter_by(active=1, uid=json['uid']).first()
        item.title=json['title']
        item.description=json['description']
        item.price=json['price']
        
        menu_item=MenuItem.query.filter_by(active=1, items_uid=json['uid']).first()
        menu_item.menus_uid=menus_uid


    @login_required
    def delete(self, uid):
        menus_uid=request.args.get('menus_uid')
        if menus_uid is None:
            abort(400, 'Missing menus_uid parameter. Not allowed to delete items without a menu to be referenced')
        
        self.delete_entity(MenuItem, active=1, items_uid=uid, menus_uid=menus_uid)
        return self.delete_response()

app = Blueprint('menus',__name__,template_folder='templates')


register_api(app,MenuService, 'menuService','/menus/','uid')
register_api(app,MenuItemsService, 'menuItemService','/menuItems/','uid')



# apps.members.models
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Menu(db.Model):
    __tablename__='menus'
    uid = db.Column(db.String(36),primary_key=True)
    active = db.Column(db.Boolean, default=1)
    title = db.Column(db.String(100), nullable=False)
    menuItems = relationship("MenuItem")

    def __init__(self,uid,title,active=1):
        self.uid = uid
        self.title = title
        self.active = active

    def __repr__(self):
        return "Menu uid=%s, title=%s, active=%s" % (self.uid, self.title, self.active)

    def as_dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name is not 'active':
                d[column.name] = getattr(self, column.name)

        return d

class Item(db.Model):
    __tablename__='items'
    uid = db.Column(db.String(36),primary_key=True)
    active = db.Column(db.Integer, default=1)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable = False)
    addon = db.Column(db.Boolean, default = False)
    menuItems = relationship("MenuItem")

    def __init__(self,uid,title,description,price,active=True,addon=False):
        self.uid = uid
        self.title = title
        self.active = active
        self.description = description
        self.price = price
        self.addon = addon

    def __repr__(self):
        return "Items uid=%s, title=%s, description=%s, price=%s, active=%s" % (self.uid, self.title, self.description, self.price, self.active)

    def as_dict(self):
        d = {}

        for column in self.__table__.columns:
            if column.name is not 'active':
                d[column.name] = getattr(self, column.name)

        return d

class MenuItem(db.Model):
    __tablename__='menus_items'
    menus_uid = db.Column(db.String(36), db.ForeignKey('menus.uid'), primary_key = True)
    items_uid = db.Column(db.String(36), db.ForeignKey('items.uid'), primary_key = True)
    active = db.Column(db.Boolean, default = True)    

    def __init__(self, menus_uid, items_uid, active=1, addon = False):
        self.menus_uid = menus_uid
        self.items_uid = items_uid
        self.active = active
        self.addon = addon

class User(db.Model):
    __tablename__='users'
    uid = db.Column(db.String(36),primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    pincode = db.Column(db.String(4),nullable=False)
    active = db.Column(db.Integer, default=1)
    groups = relationship("UserGroup")
    authenticated = True

    def __init__(self, uid,username,password,pincode,active=1):
        self.uid=uid
        self.username=username
        self.password=password
        self.pincode=pincode
        self.active=active

    def is_active(self):
        return self.active

    def get_id(self):
        return self.uid

    def is_authenticated(self):
        return self.authenticated and self.active

    def is_anonymous(self):
        return False

    def as_dict(self):
        d = {}

        for column in self.__table__.columns:
            if column.name is not 'active':
                d[column.name] = getattr(self, column.name)

        return d

class MetaUser(db.Model):
    __tablename__='meta_users'
    user_uid = db.Column(db.String(36), db.ForeignKey('users.uid'), primary_key=True)
    iteraction = db.Column(db.Integer(), nullable=False)
    product = db.Column(db.String(36), nullable=False)
    modified_on = db.Column(db.Integer(), nullable=False)

    def __init__(self, user_uid, iteraction, product, modified_on):
        self.user_uid = user_uid
        self.iteraction = iteraction
        self.product = product
        self.modified_on = modified_on


class Token(db.Model):
    __tablename__='tokens'
    user_uid = db.Column(db.String(36), db.ForeignKey('users.uid'), primary_key=True)
    token = db.Column(db.String(40), primary_key=True)
    active = db.Column(db.Integer, default=1)

    def __init__(self, user_uid, token, active=1):
        self.user_uid = user_uid
        self.token = token
        self.active = active

    def __repr__(self):
        return "Token user_uid=%s, token=%s, active=%s" % (self.user_uid, self.token, self.active)


class Group(db.Model):
    __tablename__='groups'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    active = db.Column(db.Integer, default=1)
    resourcesPermission = relationship("GroupResourcePermission")

class UserGroup(db.Model):
    __tablename__='users_groups'
    user_uid = db.Column(db.String(36), db.ForeignKey('users.uid'), primary_key=True)
    group_uid = db.Column(db.String(36), db.ForeignKey('groups.uid'), primary_key=True)

class Permission(db.Model):
    __tablename__='permissions'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    active = db.Column(db.Integer, default=1)
    resourcesPermission = relationship("GroupResourcePermission")

class Resource(db.Model):
    __tablename__='resources'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    active = db.Column(db.Integer, default=1)
    resourcesPermission = relationship("GroupResourcePermission")

class GroupResourcePermission(db.Model):
    __tablename__='group_resources_permission'
    group_uid = db.Column(db.String(36), db.ForeignKey('groups.uid'), primary_key=True)
    resource_uid = db.Column(db.String(36), db.ForeignKey('resources.uid'), primary_key=True)
    permission_uid = db.Column(db.String(36), db.ForeignKey('permissions.uid'), primary_key=True)

class State(db.Model):
    __tablename__='states'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Table(db.Model):
    __tablename__='tables'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    active = db.Column(db.Boolean, default = 1)

    def as_dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name is not 'active':
                d[column.name] = getattr(self, column.name)

        return d

    def __init__(self, uid, name, active = 1):
        self.uid = uid
        self.name = name
        self.active = active

#Association from tables and orders (Many To Many)
order_tables_assoc = db.Table('orders_tables',
                         db.Column('order_uid', db.String(36), db.ForeignKey('orders.uid')),
                         db.Column('table_uid', db.String(36), db.ForeignKey('tables.uid')))

class Order(db.Model):
    __tablename__ = 'orders'
    uid = db.Column(db.String(36), primary_key=True)
    name = name = db.Column(db.String(100))
    started_on = db.Column(db.DateTime, nullable=False)
    tables = relationship('Table', secondary=order_tables_assoc)
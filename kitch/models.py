# apps.members.models
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Menu(db.Model):
    __tablename__='menus'
    uid = db.Column(db.String(36),primary_key=True)
    active = db.Column(db.Integer, default=1)
    title = db.Column(db.String(100), nullable=False)
    menuItems = relationship("MenuItem")

    def __init__(self,uid,title,active=1):
    	self.uid = uid
    	self.title = title
    	self.active = active

    def __repr__(self):
    	return "Menu uid=%s, title=%s, active=%s" % (self.uid, self.title, self.active)

class Item(db.Model):
    __tablename__='items'
    uid = db.Column(db.String(36),primary_key=True)
    active = db.Column(db.Integer, default=1)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    menuItems = relationship("MenuItem")

    def __init__(self,uid,title,description,price,active=1):
    	self.uid = uid
    	self.title = title
    	self.active = active
    	self.description = description
    	self.price = price

    def __repr__(self):
    	return "Items uid=%s, title=%s, description=%s, price=%s, active=%s" % (self.uid, self.title, self.description, self.price, self.active)

class MenuItem(db.Model):
	__tablename__='menus_items'
	menus_uid = db.Column(db.String(36), db.ForeignKey('menus.uid'), primary_key=True)
	items_uid = db.Column(db.String(36), db.ForeignKey('items.uid'), primary_key=True)
	active = db.Column(db.Integer, default=1)

	def __init__(self, menus_uid, items_uid, active=1):
		self.menus_uid = menus_uid
		self.items_uid = items_uid
		self.active = active

class User(db.Model):
	__tablename__='users'
	uid = db.Column(db.String(36),primary_key=True)
	username = db.Column(db.String(50),nullable=False)
	password = db.Column(db.String(64),nullable=False)
	pincode = db.Column(db.String(4),nullable=False)
	active = db.Column(db.Integer, default=1)
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

class Token(db.Model):
	__tablename__='tokens'
	user_uid = db.Column(db.String(36), db.ForeignKey('users.uid'), primary_key=True)
	token = db.Column(db.String(40), primary_key=True)
	active = db.Column(db.Integer, default=1)

	def __init__(self, user_uid, token, active):
		self.user_uid = user_uid
		self.token = token
		self.active = active



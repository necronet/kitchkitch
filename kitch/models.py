# apps.members.models
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.Model):
    __tablename__='menus'
    uid = db.Column(db.String(36),primary_key=True)
    active = db.Column(db.Integer, default=1)
    title = db.Column(db.String(100), nullable=False)

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

    def __init__(self,uid,title,description,price,active=1):
    	self.uid = uid
    	self.title = title
    	self.active = active
    	self.description = description
    	self.price = price

    def __repr__(self):
    	return "Items uid=%s, title=%s, description=%s, price=%s, active=%s" % (self.uid, self.title, self.description, self.price, self.active)
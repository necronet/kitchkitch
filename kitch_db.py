import sqlite3
from flask import _app_ctx_stack
from contextlib import closing
from werkzeug.local import LocalProxy

def init_app(app):
	app.teardown_appcontext(close_database_connection)

def get_db():
	ctx = _app_ctx_stack.top
	con = getattr(ctx,'kitch_db', None)
	if con is None:
		con = sqlite3.connect(ctx.app.config['DATABASE'])
		ctx.kitch_db=con
	return con

def close_database_connection(exception):
	con = getattr(_app_ctx_stack, 'kitch_db',None)
	if con is not None:
		con.close()

#Creates local proxy pointing the database connection
db =LocalProxy(get_db)
import sqlite3
from flask import _app_ctx_stack
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

def init_db():
    with closing(get_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def close_database_connection(exception):
	con = getattr(_app_ctx_stack, 'kitch_db',None)
	if con is not None:
		con.close()

#Creates local proxy pointing the database connection
db =LocalProxy(get_db)
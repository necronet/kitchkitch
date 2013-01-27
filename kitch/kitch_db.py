from torndb import Connection
from flask import _app_ctx_stack
from werkzeug.local import LocalProxy


def init_app(app):
	app.teardown_appcontext(close_database_connection)

def get_db():
	ctx = _app_ctx_stack.top
	con = getattr(ctx,'kitch_db', None)
	if con is None:
		
		con = Connection(ctx.app.config['DB_HOST'],
                      ctx.app.config['DB_NAME'],
                      ctx.app.config['DB_USER'],
                      ctx.app.config['DB_PASSWD'])

		ctx.kitch_db=con
	return con

def close_database_connection(exception):
	con = getattr(_app_ctx_stack, 'kitch_db',None)
	if con is not None:
		con.close()

#Creates local proxy pointing the database connection
db =LocalProxy(get_db)
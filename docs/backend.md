#Todo sobre el Backend

Kitch esta creado con ciertos principios fundamentales de reutilizacion y modularizacion. 

##Sobre todo REST!

Desde el principio se oriento a ser una arquitectura orientada a servicios REST, dado su  perfecta cohesion con aplicaciones mobiles. Para mas detalles de [¿Que es REST y por que usarlo?](faq.md). 

##Flask y Python

Decir que es un Micro framework web no explica mucho, asi que realmente Flask es una alternativa muy sencilla para desarrollar aplicaciones web, a diferencia de bottle y de web2py, Flask permite modularizar mucho mas la aplicacion y no restringe trabajar el contexto en un solo archivo. 

La definición de **microframework** se comprende no por que no escala, sino por que es minimalista provee solo las herramientas basicas para **creacion de recursos y manipulacion de peitciones(request) y respuestas(response).** Los recursos en la Kitch se crean heredando de [BaseService](../kitch/utils/entities.py) y se asocia un esquema:

	class TableService(BaseService):
		schema_table = Table

El metodo get necesita un uid (unique-identifier) en caso de ubicar un recurso unico, si no es provisto entoncs se hara una consulta para obtener una lista de recursos 

	def get(self, uid):
		query_result = super(TableService, self).get(uid)

	    if type(query_result) == list:
    	   return self.get_response( [row.as_dict() for row in query_result] )
        elif type(query_result) == Table:
           return self.get_response(query_result.as_dict())

Para el metodo POST (create) [BaseService](../kitch/utils/entities.py) usara el metodo **object_from_json** y regresa una lista de recurso para persistir.

	def object_from_json(self, uid, json):
        return [Table(uid, json['name'])]

Y para el metodo PUT (update) [BaseService](../kitch/utils/entities.py) usara el metodo **update_object** y para realizar las debidas actualizaciones de un recurso:

	def update_object(self, json):
		table = Table.query.filter_by(active=1, uid=json['uid']).first()
		table.name = json['name']

### - Jinja2 & Werkzeug

Estas dos tecnologias vienen **out-of-box** con Flask, y son bases para la minimalizacion del mismo. **Jinja2** es una herramienta de creacion de plantillas del lado del servidor.  Por ejemplo **layout.html**:

	<!doctype html>
	<html land='en'>
	<title>Kitch</title>
	<link rel=stylesheet type=text/css href="{{ url_for('static', filename='css/bootstrap.css') }}">

Jinja permite la utilizacion de sentencias python dentro de llaves en este caso [url_for](http://flask.pocoo.org/docs/api/#flask.url_for) busca el url de un recurso especifico

	<script src="{{ url_for('static', filename='js/lib/jquery.js') }}"></script>
	<script src="{{ url_for('static', filename='js/lib/bootstrap.js') }}"></script>

Werkzeug provee las interfaces para WSGI, la mayor parte esta encapsulado en flask, sin embargo el comportamiento de muchos objetos de Flask es directamente dependiente de Werkzeug, en especial con:

- [Request](http://werkzeug.pocoo.org/docs/wrappers/#werkzeug.wrappers.BaseRequest)
- [Response](http://werkzeug.pocoo.org/docs/wrappers/#werkzeug.wrappers.BaseResponse)
- [Routing](http://werkzeug.pocoo.org/docs/routing/)
- [Utils](http://werkzeug.pocoo.org/docs/utils/)

### - Flask Login

[Flask-login](https://github.com/maxcountryman/flask-login/blob/master/flask_login.py) extension de flask muy util para manejar autenticar sesiones de usuarios aunque es extremadamente dependiente de las sesiones http por defecto es posible extenderlo para soportar autenticacion por token, con un par de ajustes a la forma en como se cargan los usuarios.

####¿Donde lo usamos?
Para usarlo necesitamos de registrar un LoginManager e inicializarlo:

	login_manager = CustomLoginManager()
	login_manager.init_app(app)
	login_manager.login_view = "user.loginService"

La propiedad `login_view` especifica la vista en la que el usuario se redirije en caso de no estar autenticado. (La pantalla de login).
[CustomLoginManager](../kitch/runserver.py) es la extension para permitir autenticacion por token.

Luego el LoginManager necesita de un metodo para cargara un usuario de acuerdo a un identificador:

	@login_manager.user_loader
	def load_user(uid):
	    return get_user(uid)

### - SQLAlchemy

Es un toolkit que provee capacidad para manipulacion de objetos con patron [Active Record](http://en.wikipedia.org/wiki/Active_record_pattern). Podria pensarse en un ORM lo cual lo es pero con la capacidad de poder acceder directamente a la conexion y sesion para manipular los datos de forma mas directa. En Kitch el modelo de datos [model.py](../kitch/models.py) es destinado a mantener las clases vinculadas a los esquemas.

Un ejemplo de creacion de esquemas completo:

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
		order_tables_assoc = 	db.Table('orders_tables',
								db.Column('order_uid', db.String(36), 
								db.ForeignKey('orders.uid')),
								db.Column('table_uid', db.String(36),
								db.ForeignKey('tables.uid')))


### - Test | Todo seguro
### - MakeFile
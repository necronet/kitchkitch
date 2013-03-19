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

Werkzeug provee las interfaces para WSGI.

### - Flask Login
### - SQLAlchemy
### - Test | Todo seguro
### - MakeFile
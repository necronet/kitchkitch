#Todo sobre el Backend

Kitch esta creado con ciertos principios fundamentales de reutilizacion y modularizacion. 

##Sobre todo REST!

Desde el principio se oriento a ser una arquitectura orientada a servicios REST, dado su  perfecta cohesion con aplicaciones mobiles. Para mas detalles de [¿Que es REST y por que usarlo?](faq.md). 

##Flask y Python

Decir que es un Micro framework web no explica mucho, asi que realmente Flask es una alternativa muy sencilla para desarrollar aplicaciones web, a diferencia de bottle y de web2py, Flask permite modularizar mucho mas la aplicacion y no restringe trabajar el contexto en un solo archivo. 

La definición de **microframework** se comprende no por que no escala, sino por que es minimalista provee solo las herramientas basicas para **creacion de recursos y manipulacion de peitciones(request) y respuestas(response).**


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
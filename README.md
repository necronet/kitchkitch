
#Desarrollo Kitch API 


<br/>
**Kitch** es un API REST con el proposito de mejorar los servicios ordenes en establecimientos orientado a este enfoque, aplicable tanto a bares como restaurantes.

- - -
##Requerimientos

### - Python 2.7.x 

####Linux o OSX 

Si trabajas desde ambiente es muy probable que ya tengas instalado alguna version de python ejecuta:
	
		> python --version
		
Deberias obtener **"Python 2.7.1"	** o alguna similar.
	
####Windows

Si trabajas con windows necesitaras descargar python desde el sitio oficial <http://python.org/download/>. Asegurate que sea python 2.7.x para la version de windows que se ajuste mejor a tu ambiente.

Luego recuerda de configurar el PATH para que apunte a *C:\Python27*, este paso es necesario para tener el comando python en la consola de windows.

### - MySQL 5.x
<http://www.mysql.com/downloads/mysql/>

Kitch utiliza primariamente MySQL para almacenar informacion. Asegurate de tener instalado MySQL en tu equipo y que puedas entrar con accedo root ó algun usuario que permita creacion de esquemas.

###Ademas…

Tambien es necesario tener [**git**](http://git-scm.com/) para version de control, descargar las fuentes y hacer commits al repositorio. Para facilitar push al repositorio remoto, lee la guia oficial para [Generar llaves ssh de github](http://www.tldrlegal.com/)
<br/>

- - -

##Desplegar aplicacion localmente

Luego de instalar python y mysql, puedes obtener las fuentes del proyecto 

	git clone git@github.com:necronet/kitchkitch.git


###Estructura del proyecto
Es muy probable que si leas esto estes en el repositorio. El proyecto esta estructurado de la siguiente forma.
	
	kitchkitch
		MakeFile
		docs
		kitch
		|____default_settings.py
		|____menus
		| |______init__.py
		| |____templates
		|____requirements.txt
		|____runserver.py
		|____schema.sql
		|____static
		|____test
		|____users
		|____utils

*Si crees que algo deberia ser organizado de forma diferente siente libre de hacer dichas mejoras y detallarlas en tus commit.*

###Dependencias

Dentro del proyecto tambien hay un archivo llamado requirements.txt que define las dependencias de la plataforma

- [flask](flask.pocoo.org)
- [Flask-Login](http://packages.python.org/Flask-Login/)
- [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
- [Jinja2](http://jinja.pocoo.org/docs/)
- [Werkzeug](http://werkzeug.pocoo.org/)

Con pip puedes instalar todas las dependencias ejecutando:

	pip install -r requirements.txt

Si necesitas saber [¿como instalar pip?](#y-por-que-flask)

###Base de datos

- Crea dos bases de datos en MySQL: **kitch** y **kitch_test**
- Usa el script **schema.sql** para crear el esquema de datos. Si te sientes comodo con consola puedes usar:

		mysql -u root -p kitch < schema.sql
		mysql -u root -p kitch_test < schema.sql

El script tambien creara un usuario adicional que es kitch por ello debe ser ejecutado por priemra vez 
por root para podes conceder los permisos necesarios.

Actualmente Kitch cuenta con dos esquemas de bases de datos
	- Desarrollo (kitch)
		Cuando corres la aplicacion normal con make run o con python runserver.py
	- Suite de pruebas (kitch_test)
		Cuando ejecutas la suite de pruebas habilita Testing en la configuracion de la app.
			config['TESTING'] =True

###Ejecutando la aplicacion

Existen dos formas de comprobar que todo esta trabajando correctamente, la primera es correr la aplicacion con:

	python runserver.py
	
La seguna para hacer una prueba mas a profundidad es utilizar el script de pruebas:

	python test/suite_run.py

En caso que alguna prueba falle, reportala a <joseayerdis@gmail.com> con los respectivos detalles. 

###Usando Make

Dentro del proyecto hay un MakeFile para facilitar las tareas de pruebas con las siguientes opciones:

- clean: remover todos los archivos pyc.
- run: correr la aplicacion.
- test: ejecutar la suite de pruebas.
	si necesitas ejecutar una prueba especifica utiliza el parametro SUITE=nombre_prueba
docs: crear la documentacion desde el markdown. 


##Preguntas frecuentes

###<a name="why-not-java">¿Por que no Java y/o plataformas mas familiares pare el equipo?</a>
Es una de las inquietudes que se presentan con frecuencia es ¿por que no Java?, despues de todos los miembros del proyecto actualmente somos mas Java boys. 

Pues la historia va algo asi, inicialmente Kitch fue concebido con Java, la combinacion de Jersey + Spring + Gradle + Jetty que es un contenedor que soporta JSF 2.0 nuestra marillosa tecnologia de front-end y backend todo en uno solo. Pero conforme mas pasaba, mas me daba cuenta de X siguientes fallas:

- Altamente dependiente del IDE, si bien gradle mejoro algunas cosas con el plugin de eclipse configurado, podria haberlo hecho para IntelliJ pero no tan bien para Netbeans y muchos usan Netbean. Ademas Eclipse era lento y la compilacion cada vez tardaba mas, en un prototipo que apenas iniciaba!!!.

- Hibernate es un viejo conocido de nosotros, y no creo ser el primero que detesta el merging de sesiones, el manejo de los lazy collection y mas aun HQL; podriamos discutir todo el dia de las maravillas del API de filter que tiene en el fondo sabemos los problemas que nos ha dado y lo horrible que es trabajar con ellos.

- DAO's lo menos OO y reusable que conozco en Patrones de diseños. Update, delete, get, insert Si somos intelignetes hacemos el update/insert en ambos pero igual hacemos lo mismo una y otra y otra vez. Podriamos haber visto el EntityManager que es una excelente implementacion que propone desaparecer los DAO's pero ya no tengo energias para seguir eligiendo entre JPA, Hibernate, iBatis etc.

- ActiveJDBC como no queria lidiar con hibernate, este lightweight project era prometedor Active Record como patron de persitencia se escuchaba logico, sin embargo para hacer funcionar ActiveJDBC debes ejecutar un comando que dinamicamente cambia el .class era engorroso hacerlo funcionar en la Web.

Conclusion: Java durante estos años me ha forzado a buscar alternativas hoy encontre Flask despues de probar appengine, bottle y Spark, este se escuchaba increiblemente sencillo en todo caso no todo esta escrito en piedra y si necesitamos crear otras aplicaciones y java podra ser una opcion mas popular, lo haria sin dudarlo.

Nota: En cuanto a un uso muy interesante es el uso de JasperReport para los reportes iniciales.


###<a name="y-por-que-flask">¿Y Por que Flask?</a>

Flask es un framework de traer tus herramientas a él. Por tanto provee un entorno bastante flexible si estas dispuesto a ensuciarte las manos por el proyecto. Evalue personalmente bottle, sinatra y otras combinaciones con Java como Jersey, sin embargo eran o muy simplista o demasiados complejos en cuanto a las dependencias, flask resulto ser un muy buen punto medio, y nos provee la oportunidad de 

###<a name="#install-pip">¿Como instalar pip?</a>

Existen muchas formas de instalar pip. Si estas en linux o en OSX, intenta usar el comando.
	
	easy_install pip 
	
En caso de estar en **windows** necesitas seguir los siguientes pasos:

- Descarga la version de [easy install](http://pypi.python.org/pypi/setuptools) para windows. 
- Descarga [pip](http://pypi.python.org/pypi/pip#downloads)
- Descomprimela el contenido de pip en la carpeta de C:\Python2.x\ (Recuerda solo el contenido )
- Ejecuta en la la carpeta - C:\Python2x\ - el comando
		
		python setup.py install
- Por ultimo agrega C:\Python2.x\Scripts a tu PATH de windows.

Y disfruta de pip.!!!


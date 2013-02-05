
#Desarrollo Kitch API 


<br/>
**Kitch** es primariamente un API REST orientado a mejorar los servicios ordenes en restaurantes.
- - -
##Requerimientos

###- Python 2.7.x 

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

### - Torndb
Es un proyecto que encapsula parte de la sentencias MySQL-python y crea objetos dinamicos a partir de select-statement. Para hacer uso del proyecto debes descargarlo con [github](git@github.com:necronet/torndb.git) o simplemente descarga el [proyecto](https://github.com/necronet/torndb).

Luego ejecuta dentro de la carpeta de torndb:
	
	python setup.py install

`Nota es muy probable que durante el desarrollo se incorpore torndb para acoplarlo mejor a Kitch.`

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
		|____kitch.db
		|____kitch_db.py
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
- [MySQL-python](http://pypi.python.org/pypi/MySQL-python)
- [Jinja2](http://jinja.pocoo.org/docs/)
- [Werkzeug](http://werkzeug.pocoo.org/)

Con pip puedes instalar todas las dependencias ejecutando ([como instalar pip](#install-pip) ):

	pip install -r requirements.txt

[Torndb](https://github.com/necronet/torndb) no esta en el archivo de requirements.txt pero aun asi es una dependencia que hablamos en la seccion de requerimientos.

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


##Problemas frecuentes

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


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


###Aparece TypeError Decimal('23.00') 

Si obtienes la siguiente traza (stack):

	TypeError: Decimal('23.00') is not JSON serializable
	Traceback (most recent call last)
	File "/Library/Python/2.7/site-packages/flask/app.py", line 1701, in __call__
	return self.wsgi_app(environ, start_response)
	File "/Library/Python/2.7/site-packages/flask/app.py", line 1689, in wsgi_app
	response = self.make_response(self.handle_exception(e))

El problema es que no tienes la ultima version de flask 0.10, por tanto no puede ejecutar el Custom Encoder para el tipo de dato decimal. 

	app.json_encoder = APIEncoder

La solucion es obtener la version >= 0.10 de flask. 

###¿ Que es REST y porque usarlo ?

REST es un conjunto de principios para crear servicios a base de recursos, en vez de tener multiples servicios como ***getXXX ó setXXX ó createXXX* ** los cuales no son flexibles y tienen un solo objetivo, la arquitecturas REST proponen reutilizar los mismos identificador unico de recurso (URI) y aplicar acciones a ellos usualmente con el protocolo Verbos de HTTP (GET, POST, PUT & DELETE)  (Sin embargo REST no esta sujeto a utilizar http).

Dos recursos importantes para leer con detenimiento. 

[Explicarle REST a mi esposa](http://tomayko.com/writings/rest-to-my-wife)
[REST para perros](http://vimeo.com/17785736)

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

##Obtén la fuente

Luego de instalar python y mysql, puedes obtener las fuentes del proyecto 

	git clone git@github.com:necronet/kitchkitch.git

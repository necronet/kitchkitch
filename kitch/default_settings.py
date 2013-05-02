import os

# configuration for test development
DATABASE = os.path.join (os.path.dirname(__file__) ,'kitch.db')
DEBUG = True
SECRET_KEY = '721cbaec82bf531f8f29700d994d7407e8d96087'
DB_HOST=os.getenv('OPENSHIFT_MYSQL_DB_HOST', 'localhost')
DB_PORT = os.getenv('OPENSHIFT_MYSQL_DB_PORT', '3306')
DB_NAME='kitch'
DB_NAME_TEST='kitch_test'
DB_USER=os.getenv('	', 'kitch')
DB_PASSWD=os.getenv('OPENSHIFT_MYSQL_DB_PASSWORD', 'kitch')
AUTO_COMMIT=False
UPLOAD_FOLDER = os.path.join (os.path.dirname(__file__) ,'uploads')

#TODO: do this better and automated way we will probably split
# the files for deployment in Openshift vs local platform.


#e.g mysql://kitch_user:kitch_pwd@localhost:3306/kitch
SQLALCHEMY_DATABASE_URI='mysql://%s:%s@%s:%s/%s' % (DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME)

#Test if unix socket is defined only for openshift
UNIX_SOCKET = os.getenv('OPENSHIFT_MYSQL_DB_SOCKET')
if UNIX_SOCKET:
	SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI + "?unix_socket=" + UNIX_SOCKET

import os

# configuration
DATABASE = os.path.join (os.path.dirname(__file__) ,'kitch.db')
DEBUG = True
SECRET_KEY = '721cbaec82bf531f8f29700d994d7407e8d96087'
DB_HOST='localhost'
DB_NAME='kitch'
DB_NAME_TEST='kitch_test'
DB_USER='kitch'
DB_PASSWD='kitch'
AUTO_COMMIT=False
from setuptools import setup

#TODO: try to create this automatically with requirements.txt or viceversa
setup(name='Kitch',
      version='0.1',
      description='Kitch App',
      author='Jose Ayerdis',
      author_email='joseayerdis@possol.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['itsdangerous','jinja2','MySQL-Python','werkzeug','flask==0.9','Flask-Login','Flask-SQLAlchemy'],
     )
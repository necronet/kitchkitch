from setuptools import setup

setup(name='Kitch', version='1.0',
      description='Kitch POS application',
      author='Jose Ayerdis', author_email='posol.dev@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['jinja2','MySQL-Python','werkzeug','flask==0.9','Flask-Login','Flask-SQLAlchemy'],
     )



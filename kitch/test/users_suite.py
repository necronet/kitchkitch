import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app
import unittest
from base import login

class UsersTest(unittest.TestCase):

	def setUp(self):
		self.c= app.test_client()
		app.config['TESTING'] = True

	def test_login_wrong_pasword(self):
		
		rv=login(self.c,"admin","wrongpassword")
			
		#assert rv.headers['Location'] in '/login/'
		assert rv.status_code == 401

	def test_login_right_password(self):
		
		rv=login(self.c,"admin","admin")
		assert rv.status_code == 200
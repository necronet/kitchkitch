import json
import unittest
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app

class BaseTest(unittest.TestCase):

	def setUp(self):
		self.c= app.test_client()

	def tearDown(self):
		pass

class GeneralTest(BaseTest):

	def test_empty_data_post(self):
		rv = self.c.post('/menus/',data=json.dumps({}),content_type='application/json')
		assert '400' in rv.status

	def test_wrong_data_post(self):
		rv = self.c.post('/menus/', data=json.dumps({"randonm":"items","goes":"here"}),content_type='application/json')
		assert '400' in rv.status

	def test_random_resource(self):
		rv = self.c.post('/random_non_existing_resource/')
		assert '404' in rv.status


class UsersTest(BaseTest):
	def test_login_wrong_pasword(self):
		rv=self.c.post('/login/',data=json.dumps({"username":"admin","password":"wonrg_password_goes"}),content_type='application/json')
		print rv.data
		assert rv is not None

if __name__ == '__main__':
    unittest.main()
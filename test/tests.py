import json
import unittest
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app, request

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
		with app.test_client() as client:
			rv=login(client,"admin","wrongpassword")
			
			assert rv.headers['Location'] == request.url
			assert '401' in rv.status 

	def test_login_right_password(self):
		with app.test_client() as client:
			rv=login(client,"admin","admin")
			assert '200' in rv.status


class MenuTest(BaseTest):
	def test_list_menus(self):
		with app.test_client() as client:
			rv=login(client,"admin","admin")
		
		response = json.loads(rv.data)
		token=response['token']
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',token)])
		
		assert '200' in rv.status

def login(client, username, password):
	rv=client.post('/login/',data=json.dumps({"username":username,"password":password}),content_type='application/json')
	return rv

if __name__ == '__main__':
    unittest.main()
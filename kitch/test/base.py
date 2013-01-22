import unittest
import json
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app


def login(client, username, password):
	rv=client.post('/login/',data=json.dumps({"username":username,"password":password}),content_type='application/json')
	return rv

class BaseTest(unittest.TestCase):

	def setUp(self, url=None):
		self.c= app.test_client()
		self.url = url
		app.config['TESTING'] = True
		

	def tearDown(self):
		pass
	
	def build_url(self, url=None,**kwargs):
		params=''	
		for name, value in kwargs.items():
			params += '%s=%s&' % (name, value)
			
		
		return '%s?%s' % (self.url if url is None else url ,params)
	
	def post():
		return self.c.post(self.build_url(),data=json.dumps({}),content_type='application/json')

class GeneralTest(BaseTest):

	def setUp(self):
		super(GeneralTest,self).setUp('/menus/')
		

	def test_empty_data_post(self):
		rv = self.post()
		assert rv.status_code == 400

	def test_wrong_data_post(self):
		rv = self.c.post(self.build_url(), data=json.dumps({"randonm":"items","goes":"here"}),content_type='application/json')
		assert rv.status_code == 400

	def test_random_resource(self):
		rv = self.c.post(self.build_url(url='/random_non_existing_resource/'), data=json.dumps({'items':[{"randonm":"items","goes":"here"}]}),content_type='application/json')
		assert rv.status_code == 404

	def test_wrong_mime(self):
		rv = self.c.post('/menus/')
		assert rv.status_code == 415

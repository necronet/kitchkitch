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
	
	def post(self,url=None,data=json.dumps({}),content_type='application/json',**kwargs):
		return self.c.post(self.build_url(url=url,**kwargs),data=data,content_type=content_type)

	def get(self, url=None, headers=[('Accept','application/json')],**kwargs):
		return self.c.get(self.build_url(url=url,**kwargs),headers=headers)

class GeneralTest(BaseTest):

	def setUp(self):
		super(GeneralTest,self).setUp('/menus/')

	def test_empty_data_post(self):
		rv = self.post()
		assert rv.status_code == 400

	def test_wrong_data_post(self):
		rv = self.post(data=json.dumps({"randonm":"items","goes":"here"}))
		assert rv.status_code == 400

	def test_random_resource(self):
		rv = self.post(url='/imaginary_resource/',data=json.dumps({'items':[{}]}))
		assert rv.status_code == 404

	def test_wrong_mime(self):
		rv = self.post(content_type='text/html')
		assert rv.status_code == 415

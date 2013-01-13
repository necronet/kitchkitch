import json
import unittest
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app

class GeneralTest(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_empty_data_post(self):
		with app.test_client() as c:
			rv = c.post('/login/')
			assert '400' in rv.status

	def test_wrong_data_post(self):
		with app.test_client() as c:
			rv = c.post('/login/', data=json.dumps({"username":"admin","password":"password"}),content_type='application/json')
			assert '400' in rv.status


if __name__ == '__main__':
    unittest.main()
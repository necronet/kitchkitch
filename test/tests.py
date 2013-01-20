import json
import unittest
import os,sys
import tests_users
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app

class BaseTest(unittest.TestCase):

	def setUp(self):
		self.c= app.test_client()

		app.config['TESTING'] = True
		

	def tearDown(self):
		pass

class GeneralTest(BaseTest):

	def test_empty_data_post(self):
		rv = self.c.post('/menus/',data=json.dumps({}),content_type='application/json')
		assert rv.status_code == 400

	def test_wrong_data_post(self):
		rv = self.c.post('/menus/', data=json.dumps({"randonm":"items","goes":"here"}),content_type='application/json')
		assert rv.status_code == 400

	def test_random_resource(self):
		rv = self.c.post('/random_non_existing_resource/', data=json.dumps({'items':[{"randonm":"items","goes":"here"}]}),content_type='application/json')
		assert rv.status_code == 404

	def test_wrong_mime(self):
		rv = self.c.post('/menus/')
		assert rv.status_code == 415



class MenuTest(BaseTest):

	def setUp(self):
		super(MenuTest,self).setUp()
		with app.test_client() as client:
			rv=login(client,"admin","admin")
		
		response = json.loads(rv.data)
		self.token=response['token']

	def test_list_menus(self):
		
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',self.token)])
		assert rv.status_code == 200

	def test_post(self):
		rv=self.c.post('/menus/',data=json.dumps({"items":[{"title":"Menu #1"}]}),content_type='application/json')
		assert rv.status_code == 201

	def test_put(self):
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',self.token)])
		
		assert rv.status_code == 200
		items=json.loads(rv.data)
		assert len(items) > 0

		new_items=[]
		for data in items['items']:
		  new_items.append({'uid':data['uid'],'title':data['title']+' Modified'})
		
		items['items']=new_items
		rv=self.c.put('/menus/',data=json.dumps(items),content_type='application/json')
		assert rv.status_code == 200
	
	def test_list_menus_filters(self):
		rv=self.c.get('/menus/?title=Menu #1,Menu #2',headers=[('Accept','application/json'),('Authorization',self.token)])
		
		assert rv.status_code == 200
		

	def test_delete_menus(self):
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',self.token)])
		
		assert rv.status_code == 200
		items=json.loads(rv.data)

		for data in items['items']:
			rv=self.c.delete('/menus/%s' % data['uid'],content_type='application/json')
		
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',self.token)])
		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

class MenuItemService(BaseTest):
	def test_list_menu_items(self):
		rv=self.c.get('/menuItems/',headers=[('Accept','application/json')])		
		
		assert rv.status_code==200

	def test_post_menus_missing_menu_uid(self):
		menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}
		rv=self.c.post('/menuItems/',data=json.dumps(menu_items),content_type='application/json')
		assert rv.status_code == 400

	def test_post(self):
		rv=self.c.get('/menus/',headers=[('Accept','application/json')])
		
		uid=json.loads(rv.data)['items'][0]['uid']		

		menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}

		rv=self.c.post('/menuItems/?menus_uid=%s'%uid,data=json.dumps(menu_items),content_type='application/json')
		assert rv.status_code == 201

	def test_put(self):
		rv=self.c.get('/menuItems/',headers=[('Accept','application/json')])
		menu_item=json.loads(rv.data)['items'][0]
		update_data = {'items':[{'uid':menu_item['uid'],'title':menu_item['title'],'description':menu_item['description'],'price':menu_item['price']}]}
		
		rv=self.c.put('/menuItems/',data=json.dumps(update_data),content_type='application/json')		
		print rv.data

	def test_delete_items(self):
		rv=self.c.get('/menus/',headers=[('Accept','application/json')])
		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		items=json.loads(rv.data)['items']
		menus_uid=items[0]['uid']
		rv=self.c.get('/menuItems/menus_uid=%s'%menus_uid,headers=[('Accept','application/json')])

		for data in json.loads(rv.data)['items']:
			rv=self.c.delete('/menusItems/%s' % data['uid'],content_type='application/json')
		
		rv=self.c.get('/menuItems/menus_uid=%s'%menus_uid,headers=[('Accept','application/json')])

		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

		#rv=self.c.delete('/menus/%s' % data['uid'],content_type='application/json')



def login(client, username, password):
	rv=client.post('/login/',data=json.dumps({"username":username,"password":password}),content_type='application/json')
	return rv


if __name__=='__main__':
	runTests=[GeneralTest,tests_users.UsersTest,MenuTest]

	for runTest in runTests:
		suite = unittest.TestLoader().loadTestsFromTestCase(runTest)
		unittest.TextTestRunner(verbosity=2).run(suite)
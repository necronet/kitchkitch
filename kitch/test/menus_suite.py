import json
from base import BaseTest, login

class MenuTest(BaseTest):

	def setUp(self):
		super(MenuTest,self).setUp('/menus/')
		rv=login(self.c,"admin","admin")
		
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
			assert rv.status_code==202
		
		rv=self.c.get('/menus/',headers=[('Accept','application/json'),('Authorization',self.token)])
		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

class MenuItemTest(BaseTest):

	def setUp(self):
		super(MenuItemTest,self).setUp('/menuItems/')
		rv=login(self.c,"admin","admin")
		
		response = json.loads(rv.data)
		self.token=response['token']

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
		rv=self.c.get('/menus/',headers=[('Accept','application/json')])
		menus_uid=json.loads(rv.data)['items'][0]['uid']
		
		rv=self.c.get('/menuItems/?menus_uid=%s' % menus_uid,headers=[('Accept','application/json')])
		
		menu_item=json.loads(rv.data)['items'][0]
		update_data = {'items':[{'uid':menu_item['uid'],'title':menu_item['title'],'description':menu_item['description'],'price':menu_item['price']}]}
		
		rv=self.c.put('/menuItems/?menus_uid=%s' % menus_uid ,data=json.dumps(update_data),content_type='application/json')		
		assert rv.status_code == 200

	def test_delete_items(self):
		rv=self.c.get('/menus/',headers=[('Accept','application/json')])
		assert rv.status_code == 200
		items=json.loads(rv.data)['items']
		menus_uid=items[0]['uid']
		
		rv=self.c.get('/menuItems/?menus_uid=%s'% menus_uid ,headers=[('Accept','application/json')])

		for data in json.loads(rv.data)['items']:

			rv=self.c.delete('/menuItems/%s?menus_uid=%s' % (data['uid'],menus_uid),content_type='application/json')
			assert rv.status_code == 202
		
		rv=self.c.get('/menuItems/?menus_uid=%s'%menus_uid,headers=[('Accept','application/json')])

		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

		#rv=self.c.delete('/menus/%s' % data['uid'],content_type='application/json')
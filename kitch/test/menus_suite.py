import json
from base import BaseTest

class MenuTest(BaseTest):

	def setUp(self):
		super(MenuTest,self).setUp('/menus/')	

	def test_post(self):
		rv=self.post(data=json.dumps({"items":[{"title":"Menu #1"}]}))
		assert rv.status_code == 201

	def test_get_item(self):
		self.check_item(json.dumps({"items":[{"title":"Menu #1"}]}),('uid','title'))

	def test_put(self):
		rv=self.get()

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
		rv=self.get(title='Menu #1,Menu #2')
		assert rv.status_code == 200
		

	def test_delete_menus(self):
		rv=self.get()
		
		assert rv.status_code == 200
		items=json.loads(rv.data)

		for data in items['items']:
			rv=self.c.delete('/menus/%s' % data['uid'],content_type='application/json')
			assert rv.status_code==202
		
		rv=self.get()
		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

class MenuItemTest(BaseTest):

	def setUp(self):
		super(MenuItemTest,self).setUp('/menuItems/')			

	def test_post_menus_missing_menu_uid(self):
		menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}
		rv=self.c.post('/menuItems/',data=json.dumps(menu_items),content_type='application/json')
		assert rv.status_code == 400

	def test_get_item(self):
		rv=self.get(url='/menus/')
		uid=json.loads(rv.data)['items'][0]['uid']
		
		menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}
		self.check_item(json.dumps(menu_items),('uid','title'),menus_uid=uid)

	def test_post(self):
		rv=self.get(url='/menus/')
		
		uid=json.loads(rv.data)['items'][0]['uid']		
		
		menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}
		rv=self.post(data=json.dumps(menu_items),menus_uid=uid)
		assert rv.status_code == 201	

	def test_put(self):
		rv=self.get(url='/menus/')
		menus_uid=json.loads(rv.data)['items'][0]['uid']
		
		rv=self.get(url='/menuItems/',menus_uid=menus_uid)
		
		menu_item=json.loads(rv.data)['items'][0]
		update_data = {'items':[{'uid':menu_item['uid'],'title':menu_item['title'],'description':menu_item['description'],'price':menu_item['price']}]}
		
		rv=self.c.put('/menuItems/?menus_uid=%s' % menus_uid ,data=json.dumps(update_data),content_type='application/json')		
		assert rv.status_code == 200

	def test_delete_items(self):
		rv=self.get(url='/menus/')
		assert rv.status_code == 200
		items=json.loads(rv.data)['items']
		menus_uid=items[0]['uid']
		
		rv=self.get(menus_uid=menus_uid)

		for data in json.loads(rv.data)['items']:

			rv=self.c.delete('/menuItems/%s?menus_uid=%s' % (data['uid'],menus_uid),content_type='application/json')
			assert rv.status_code == 202
		
		rv=self.get(menus_uid=menus_uid)

		assert rv.status_code == 200
		items=json.loads(rv.data)
		
		assert len(items['items']) == 0

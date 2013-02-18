import json
from base import BaseTest

class MenuTest(BaseTest):

    def setUp(self):
        super(MenuTest,self).setUp('/menus/',auth=True)

    def test_get(self):
        response=super(MenuTest,self).test_get()
        for row in response:
            assert row.has_key('items')


    def test_post(self):
        rv=self.post(data=json.dumps({"title":"Menu #1"}))
        assert rv.status_code == 201

    def test_get_item(self):
        response_object=self.check_item(json.dumps({"items":[{"title":"Menu #1"}]}),['uid','title'])
        assert response_object.has_key('items')

    def test_put(self):
        rv=self.get()

        assert rv.status_code == 200
        items=json.loads(rv.data)
        assert len(items) > 0

        
        for data in items['items']:
            rv=self.put(data=json.dumps({'uid':data['uid'],'title':data['title']+' Modified'}))
            assert rv.status_code == 200

    def test_list_menus_filters(self):
        rv=self.get(title='Menu #1,Menu #2')
        assert rv.status_code == 200


    def test_delete_menus(self):
        rv=self.get()

        assert rv.status_code == 200
        items=json.loads(rv.data)

        for data in items['items']:
            rv=self.delete(data['uid'])

            assert rv.status_code==202

        rv=self.get()
        assert rv.status_code == 200
        items=json.loads(rv.data)

        assert len(items['items']) == 0

class MenuItemTest(BaseTest):

    def setUp(self):
        super(MenuItemTest,self).setUp('/menuItems/',auth=True)

    def test_post_menus_missing_menu_uid(self):
        menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}
        rv=self.post(json.dumps(menu_items))
        assert rv.status_code == 400

    def test_get_item(self):
        rv=self.get(url='/menus/')

        uid=json.loads(rv.data)['items'][0]['uid']

        menu_items={"items":[{"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}]}

        self.check_item(json.dumps(menu_items),['uid','title'],menus_uid=uid)

        

    def test_get_menu_with_expand(self):
        #Make items
        self.test_post()
        rv=self.get(url='/menus/', expand='items')

        for row in json.loads(rv.data)['items']:
            assert row.has_key('items')

    def test_get_single_menu_with_expand(self):
        #Make items
        rv=self.get(url='/menus/')

        uid=json.loads(rv.data)['items'][0]['uid']
        self.test_post()

        rv=self.get(url='/menus/',uid=uid, expand='items')


        for row in json.loads(rv.data)['items']:
            assert row.has_key('title')
            assert row.has_key('price')
            assert row.has_key('uid')

    def test_post(self):
        rv=self.get(url='/menus/')

        uid=json.loads(rv.data)['items'][0]['uid']

        menu_items={"title":"Menu Items #1",'description':'delicous meal to serve','price':10.25}
        rv=self.post(data=json.dumps(menu_items),menus_uid=uid)
        assert rv.status_code == 201

    def test_put(self):
        rv=self.get(url='/menus/')
        menus_uid=json.loads(rv.data)['items'][0]['uid']

        rv=self.get(url='/menuItems/',menus_uid=menus_uid)

        menu_item=json.loads(rv.data)['items'][0]
        update_data = {'uid':menu_item['uid'],'title':menu_item['title']+' modified','description':menu_item['description'],'price':menu_item['price']}

        rv=self.put(data=json.dumps(update_data),menus_uid=menus_uid )
        assert rv.status_code == 200

    def test_delete_items(self):
        rv=self.get(url='/menus/')
        assert rv.status_code == 200
        items=json.loads(rv.data)['items']
        menus_uid=items[0]['uid']

        rv=self.get(menus_uid=menus_uid)

        for data in json.loads(rv.data)['items']:

            rv=self.delete(data['uid'],menus_uid=menus_uid)
            assert rv.status_code == 202

        rv=self.get(menus_uid=menus_uid)

        assert rv.status_code == 200
        items=json.loads(rv.data)

        assert len(items['items']) == 0

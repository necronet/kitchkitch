from base import BaseTest
import json
import random

class TableTest(BaseTest):
    def setUp(self):
        super(TableTest, self).setUp('/table/',auth=True)

    def test_post(self):
        n = random.randint(0,50000000)
        rv=self.post(data=json.dumps({"name":"#1%s" % n }))
        assert rv.status_code == 201

    def test_get_item(self):
        self.check_item(['uid','name'])

    def test_put(self):
        """
            Test the update of a User resource by 
            retrieving items from it and picking a random user. 
            and then updating it's pincode and password.
            
            - Assert the response is 200 
            - that the usermay login with it's new credential
        """
        self.test_post()

        items=self.test_get()
        assert len(items) > 2

        #Get the first table
        table = items[0]

        table['name'] = table['name']+' modified'

        rv=self.put(data=json.dumps(table))

        assert rv.status_code == 200

    def test_delete_menus(self):
        rv=self.get()

        assert rv.status_code == 200
        items=json.loads(rv.data)

        for data in items['items']:
            rv=self.delete(data['uid'])

            assert rv.status_code==204

        rv=self.get()
        assert rv.status_code == 200
        items=json.loads(rv.data)
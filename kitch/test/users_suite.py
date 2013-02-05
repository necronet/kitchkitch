import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app
import unittest
from base import login, BaseTest
import json
import random

class UserTest(BaseTest):

    def setUp(self):
        super(UserTest,self).setUp('/user/',auth=True)

    def test_get(self):
        rv=self.get()        
        assert rv.status_code == 200
        response_data = json.loads(rv.data)['items']
        assert len(response_data)        
        for item in response_data:
            assert item['href'] is not None

        return response_data
    def test_get_item(self):
        response_object=self.check_item({
                                        'username':'necronet%d' % random.randint(0,500000000),
                                        'password':'necronet',
                                        'pincode':'0000'},['uid','username','pincode'])

    def test_post(self):
        #it is likely that this might failed 1 in 50 million that why such a big number
        data=json.dumps({'username':'necronet%d' % random.randint(0,500000000),'password':'necronet','pincode':'0000'})
        rv=self.post(data=data)        
        assert rv.status_code == 201

    def test_put(self):
        
        items=self.test_get()
        assert len(items) > 0

        user=items[random.randint(1,len(items)-1)]

        user['pincode']='8989'
        user['password']='admin'
        rv=self.put(data=json.dumps(user))
        assert rv.status_code == 200

    def test_post_conflict(self):
        data=json.dumps({'username':'admin','password':'something','pincode':'0000'})
        rv=self.post(data=data)        
        assert rv.status_code == 409
    

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.c= app.test_client()
        app.config['TESTING'] = True


    def test_login_wrong_pasword(self):
        rv=login(self.c,"admin","wrongpassword")
        assert rv.status_code == 401

    def test_login_right_password(self):
        rv=login(self.c,"admin","admin")
        assert rv.status_code == 200

    def test_logout(self):
        rv=login(self.c,"admin","admin")
        self.auth_token=json.loads(rv.data)['token']
        rv=self.c.delete('/login/%s'% self.auth_token,content_type='application/json',headers=self.config_headers([]))
        assert rv.status_code == 202

    def test_empty_user_and_password(self):
        rv=login(self.c,"","admin")
        assert rv.status_code == 400
        rv=login(self.c,"admin","")
        assert rv.status_code == 400
        rv=login(self.c,"","")
        assert rv.status_code == 400

    def test_get_login(self):
        rv=self.c.get('/login/', content_type='application/json',headers=[('Accept','application/json')])
        assert rv.status_code==501

    def config_headers(self, headers):
        if headers is None:
            headers=[('Accept','application/json')]
        if self.auth_token is not None:
            headers.append(('Authorization',self.auth_token))

        return headers

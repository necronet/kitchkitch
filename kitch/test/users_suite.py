import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 
from runserver import app
import unittest
from base import login, BaseTest
import json

class UserTest(BaseTest):
    def test_get(self):
        pass

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

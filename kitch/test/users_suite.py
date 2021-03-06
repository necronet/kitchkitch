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
    """
        Test method related to users. Inherit from BaseTest so there are some default 
        testing behaviour.
    """

    def setUp(self):
        super(UserTest,self).setUp('/user/',auth=True)

    def test_get(self):
        """
            Test the GET method and ensure a 200 OK response 
            and href self reference is there.
        """
        rv=self.get()
        assert rv.status_code == 200
        response_data = json.loads(rv.data)['items']
        assert len(response_data)>0
        #for item in response_data:
        #    assert item['href'] is not None

        return response_data

    def test_get_item(self):
        """
            Test the retribution of a single user using inherit method
            check_item, will pass a object so that it can be created 
            and then retrieve it single instance using GET

            Checks that the retrieve response conains uid, username, pincode.
        """
        response_object=self.check_item(['uid','username','pincode'])

    def test_post(self,username=None):
        """
            Create a random user with password necronet and pincode '0000'
            Ensure that the response is 201.
        """
        #it is likely that this might failed 1 in 50 million that why such a big number
        
        if not username:
            username='necronet%d' % random.randint(0,500000000)
        data=json.dumps({'username':username,'password':'necronet','pincode':'0000'})
        rv=self.post(data=data)        
        assert rv.status_code == 201
        

    def test_put(self):
        """
            Test the update of a User resource by 
            retrieving items from it and picking a random user. 
            and then updating it's pincode and password.
            
            - Assert the response is 200 
            - that the usermay login with it's new credential
        """
        username='necronet%d' % random.randint(0,500000000)
        self.test_post(username)

        items=self.test_get()
        assert len(items) > 2

        user = None
        for user in items:
            if user['username'] == username:
                break


        rv = login(self.c,username,"necronet")

        self.auth_token=json.loads(rv.data)['token']

        user['pincode']='8989'
        user['password']='admin'
        rv=self.put(data=json.dumps(user))

        assert rv.status_code == 403

        #Check that the record changed can login with the new password
        #rv=login(self.c,user['username'],"admin")
        #assert rv.status_code == 200

    def test_delete_users(self):
        """
            Get all users and delete them. Making sure that does not delete the administrative profile.
            Assert that in the response is a 204 Accepted.
        """
        items=self.test_get()

        for data in items:
            if data['username'] == 'admin': continue
            
            rv=self.delete(data['uid'])
            
            assert rv.status_code==204

    def test_post_conflict(self):
        '''
            Test the creation of a user that already exist in the system.
        '''
        data=json.dumps({'username':'admin','password':'something','pincode':'0000'})
        rv=self.post(data=data)        
        assert rv.status_code == 409
    

class LoginTest(unittest.TestCase):
    """
        Test login resources in general. This is a very special resources that will return
        authentication token to make calls that required system authorization.

        Note: also note that this Test does not inherit from BaseTest since it will not need for all the 
        inherit method from it.
    """
    def setUp(self):
        """
            Set up configuration for the test create an test client and 
            configure the application in TESTING mode.
        """
        self.c= app.test_client()
        app.config['TESTING'] = True

    def test_login_wrong_user_and_pasword(self):
        """
            Try to login using a wrong password.
            Assert that the response is a 401.
        """
        rv=login(self.c,"wrongusername","wrongpassword")
        assert rv.status_code == 401


    def test_login_wrong_pasword(self):
        """
            Try to login using a wrong password.
            Assert that the response is a 401.
        """
        rv=login(self.c,"admin","wrongpassword")
        assert rv.status_code == 401

    def test_login_right_password(self):
        """
        Try to login using a correct password. The response should be 200.
        """
        rv=login(self.c,"admin","admin")
        assert rv.status_code == 200

    def test_logout(self):
        """
        Try to logout in order to do this there should be a login and a authtoken to logout.
        no need to pass any special data in the body.

        Assert that the response is a 204.
        """
        rv=login(self.c,"admin","admin")
        self.auth_token=json.loads(rv.data)['token']
        rv=self.c.delete('/login/%s'% self.auth_token,content_type='application/json',headers=self.config_headers([]))
        assert rv.status_code == 204

    def test_empty_user_and_password(self):
        """
            Test an empty username and passwod for three cases and assert
            400 Bad request for each case.
        """
        rv=login(self.c,"","admin")
        assert rv.status_code == 400
        rv=login(self.c,"admin","")
        assert rv.status_code == 400
        rv=login(self.c,"","")
        assert rv.status_code == 400

    def test_get_login(self):
        """
            Test getting the login records, since this is an unimplementend resource, should return
            501 not implemented. 
            
        """
        rv=self.c.get('/login/', content_type='application/json',headers=[('Accept','application/json')])
        assert rv.status_code==501

    def test_put_login(self):
        """
            Test modifyinh a login record, since this is an unimplementend resource, should return
            501 not implemented.
        """
        rv=self.c.put('/login/', data=json.dumps({"username":'',"password":''}), content_type='application/json',headers=[('Accept','application/json')])

        assert rv.status_code==501

    def config_headers(self, headers):
        if headers is None:
            headers=[('Accept','application/json')]
        if self.auth_token is not None:
            headers.append(('Authorization',self.auth_token))

        return headers

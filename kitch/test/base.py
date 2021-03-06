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
    _auth_token=None

    def setUp(self, url=None,auth=False):
        self.c= app.test_client()
        self.url = url
        app.config['TESTING'] = True
        if auth and self.auth_token is None:
            rv = login(self.c,"admin","admin")
            self.auth_token=json.loads(rv.data)['token']

        self.clear_auth()

    def test_with_no_auth(self):
        if self.auth_token:
            self.clear_auth()
            self.auth_token=None
            rv=self.get()
            assert rv.status_code==401
            rv=self.post(data=json.dumps({'items':[]}))
            assert rv.status_code==401

    def tearDown(self):
        pass

    @property
    def auth_token(self):
        return self._auth_token

    @auth_token.setter
    def auth_token(self,value):
        self._auth_token=value

    def test_get_wrong_id(self, **kwargs):
        """
        Try to get a resources with an unexisting UID
        response 404 Not Found
        """

        rv=self.get(uid='FAKE_UID')

        assert rv.status_code == 404


    def test_get(self, **kwargs):
        """
        Insert a record
        Then it tries to retrieve a list of those records
        checking:
            - response 200 OK
            - at least there is one item in the list

        """
        self.test_post()
        rv=self.get(**kwargs)
        assert rv.status_code == 200

        response_data=json.loads(rv.data)['items']

        assert len(response_data) > 0

        return response_data
    
    def check_item(self, keys):
        """
        Basic method to check that get request with a uid
        is correct.

        - Ensure that an item is created, by doing a test_post
        - Does  GET request an append uid to it. i.e (http://localhost/menu?uid=XXXXX)
        - Assert that the response contains the keys list.

        Note: will always append 'href' to keys list.
        """
        
        self.test_post()
        rv=self.get()
        uid=json.loads(rv.data)['items'][0]['uid']
        rv=self.get(uid=uid)
        assert rv.status_code == 200
        #Check all properties are i response

        response_object=json.loads(rv.data)
        for i in keys: assert i in response_object

        return response_object

    def build_url(self, uid='',url=None,**kwargs):
        params=''
        for name, value in kwargs.items():
            params += '%s=%s&' % (name, value)


        return '%s%s?%s' % (self.url if url is None else url ,uid,params)

    def post(self,url=None,data=json.dumps({}),content_type='application/json',headers=None,**kwargs):
        return self.c.post(self.build_url(url=url,**kwargs),data=data,content_type=content_type, headers=self.config_headers(headers))

    def get(self,uid='', url=None, authorize=True, headers=None,**kwargs):
        headers = self.config_headers(headers) if authorize else headers
        return self.c.get(self.build_url(url=url,uid=uid,**kwargs),headers=headers)

    def delete(self, uid,url=None,headers=None, content_type='application/json', **kwargs):
        return self.c.delete(self.build_url(url=url,uid=uid,**kwargs), content_type=content_type,headers=self.config_headers(headers))

    def put(self,url=None,data=json.dumps({}),content_type='application/json',headers=None,**kwargs):
        return self.c.put(self.build_url(url=url,**kwargs),data=data,content_type=content_type, headers=self.config_headers(headers))

    

    def config_headers(self, headers):
        if headers is None:
            headers=[('Accept','application/json')]
        if self.auth_token is not None:
            headers.append(('Authorization',self.auth_token))

        return headers

    def clear_auth(self):
        """
        Allows to clear the authorization session currently in the test_client() objects
        by simply removing the _id and user_id from session_transaction object.
        """

        with self.c.session_transaction() as session:
            session['_id']=None
            session['user_id']=None


class GeneralTest(BaseTest):

    def setUp(self):
        super(GeneralTest,self).setUp('/menus/',auth=True)

    @unittest.skip('Not valid for general testing')
    def test_get(self):
        pass

    def test_unauthorize(self):
        rv = self.get(authorize=False, headers=[('Accept','application/json')])
        assert rv.status_code == 401

    def test_wrong_authorization(self):
        self.auth_token='wrongtoken';
        rv = self.get()
        assert rv.status_code == 401

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

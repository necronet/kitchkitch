from base import BaseTest, login
import unittest

class UsersTest(BaseTest):
	def test_login_wrong_pasword(self):
		
		rv=login(self.c,"admin","wrongpassword")
			
		#assert rv.headers['Location'] in '/login/'
		assert rv.status_code == 401

	@unittest.skip('Not valid for users module test')
	def get(self):
		pass

	def test_login_right_password(self):
		
		rv=login(self.c,"admin","admin")
		assert rv.status_code == 200
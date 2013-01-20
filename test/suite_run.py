import unittest
from base import GeneralTest
import users_suite
import menus_suite

if __name__=='__main__':
	runTests=[GeneralTest,users_suite.UsersTest,menus_suite.MenuTest,menus_suite.MenuItemTest]

	for runTest in runTests:
		suite = unittest.TestLoader().loadTestsFromTestCase(runTest)
		unittest.TextTestRunner(verbosity=2).run(suite)
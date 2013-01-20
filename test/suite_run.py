import unittest
from base import GeneralTest
import tests_users
import tests_menus

if __name__=='__main__':
	runTests=[GeneralTest,tests_users.UsersTest,tests_menus.MenuTest]

	for runTest in runTests:
		suite = unittest.TestLoader().loadTestsFromTestCase(runTest)
		unittest.TextTestRunner(verbosity=2).run(suite)
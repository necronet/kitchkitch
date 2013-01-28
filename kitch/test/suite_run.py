import argparse
import unittest
from base import GeneralTest
import users_suite
import menus_suite

if __name__=='__main__':

	tests_suite={'general':GeneralTest,'user':users_suite.UsersTest,'menu':menus_suite.MenuTest,'menu_item':menus_suite.MenuItemTest}
	parser = argparse.ArgumentParser(description="Script for testing volunteer services")
	keys_args= ('|'.join(tests_suite.keys()))
	parser.add_argument('-t', '--test',default='all',help='Test services [all|%s]. If no value is specify then it will run "all" tests' % keys_args)
	args=parser.parse_args()

	run_test=args.test.split(',')
	

	

	for key,test in tests_suite.items():
		if 'all' in run_test or key in run_test:
			suite = unittest.TestLoader().loadTestsFromTestCase(test)
			unittest.TextTestRunner(verbosity=2).run(suite)
	
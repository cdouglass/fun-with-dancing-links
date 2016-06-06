import os
import sys
import re
sys.path.insert(0, os.path.abspath('..'))
import flask
import puzzle
import unittest

class IntegrationTests(unittest.TestCase):

  def setUp(self):
    puzzle.app.config['TESTING'] = True
    self.app = puzzle.app.test_client()

  def testRootRedirectsToNQueens(self):
    response = self.app.get('/', follow_redirects = False)
    self.assertEqual(302, response.status_code)
    self.assertRegex(response.location, '/n_queens') # location is full url

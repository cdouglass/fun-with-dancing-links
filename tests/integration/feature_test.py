import os
import sys
import re
sys.path.insert(0, os.path.abspath('..'))
import puzzle
import unittest

class IntegrationTests(unittest.TestCase):

  def setUp(self):
    puzzle.app.config['TESTING'] = True # no difference yet, right?
    self.app = puzzle.app.test_client()

  def testRootLoads(self):
    response = self.app.get('/')
    self.assertEqual(200, response.status_code)

  def testRootShowsHelloWorld(self):
    response = self.app.get('/')
    self.assertRegex(response.data.decode('utf-8'), re.compile("Hello, World"))

import os
import sys
import re
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.abspath('..'))
import flask
import puzzle
import unittest

def get_contents_of_ids(body, ids):
  return {i:body.find(id=i).string for i in ids}

class NQueensIntegrationTests(unittest.TestCase):

  def setUp(self):
    puzzle.app.config['TESTING'] = True
    self.app = puzzle.app.test_client()

  def testRootLoads(self):
    response = self.app.get('/', follow_redirects = False)
    self.assertEqual(200, response.status_code)

  def testNQueensLoads(self):
    response = self.app.get('/n_queens')
    self.assertEqual(200, response.status_code)

  def testNQueensDefaultsTo4(self):
    response = self.app.get('/n_queens')
    body = BeautifulSoup(response.data, 'html.parser') # BS assumes byte strings are UTF-8
    fields = get_contents_of_ids(body, ["index", "solution_count", "n"])
    self.assertEqual('1', fields["index"])
    self.assertEqual('2', fields["solution_count"])
    self.assertEqual('4', fields["n"])

  def testNQueensWithQueryStringSucceeds(self):
    response = self.app.get('/n_queens?n=6')
    self.assertEqual(200, response.status_code)

  def testNQueensShowsNewSolutionsOnSettingBoardSize(self):
    response = self.app.get('/n_queens?n=6')
    body = BeautifulSoup(response.data, 'html.parser') # BS assumes byte strings are UTF-8
    fields = get_contents_of_ids(body, ["index", "solution_count", "n"])
    self.assertEqual('1', fields["index"])
    self.assertEqual('4', fields["solution_count"])
    self.assertEqual('6', fields["n"])

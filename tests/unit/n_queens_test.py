import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from lib.n_queens import *
import unittest

class TestMatchers(unittest.TestCase):

#  def setUp(self):

  def test_forward_diagonal_matcher_major_diagonal(self):
    matcher = forward_diag_matcher(0) # major diagonal
    self.assertTrue(matcher(0, 0))
    self.assertTrue(matcher(8, 8))
    self.assertFalse(matcher(8, 7))

  def test_forward_diagonal_matcher_positive(self):
    matcher = forward_diag_matcher(2) # major diagonal
    self.assertTrue(matcher(2, 0))
    self.assertTrue(matcher(3, 1))
    self.assertFalse(matcher(3, 0))

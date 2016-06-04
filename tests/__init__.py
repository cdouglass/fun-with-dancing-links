import unittest

def prepare_load_tests_function(the__path__):
  test_suite = unittest.TestLoader().discover(the__path__[0], '*test.py')
  return lambda _a, _b, _c: test_suite

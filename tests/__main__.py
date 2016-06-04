#! /usr/bin/env python

import unittest

# ripped from http://stackoverflow.com/questions/644821/python-how-to-run-unittest-main-for-all-source-files-in-a-subdirectory
from . import prepare_load_tests_function, __path__
load_tests = prepare_load_tests_function(__path__)
unittest.main()

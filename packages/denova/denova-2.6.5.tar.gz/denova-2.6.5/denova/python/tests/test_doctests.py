#!/usr/bin/env python3
'''
    Tests the doctests for denova.python.

    The tests starting with xtest aren't being
    maintained so have been disabled.

    Copyright 2019-2022 DeNova
    Last modified: 2022-11-18
'''

import os
import sys
from doctest import testmod
from unittest import main, TestCase

import denova.python.dict
import denova.python.elapsed_time
import denova.python.format
import denova.python.internals
import denova.python.iter
import denova.python.log
import denova.python._log
import denova.python.performance
import denova.python.text_file
import denova.python.times
import denova.python.utils

from denova.python.utils import run_module_test


class TestDoctests(TestCase):

    def test_dict(self):
        ''' Test dict doctests. '''

        run_module_test(denova.python.dict)

    def test_elapsed_time(self):
        ''' Test elapsed_time doctests. '''

        run_module_test(denova.python.elapsed_time)

    def test_format(self):
        ''' Test format doctests. '''

        run_module_test(denova.python.format)

    def test_internals(self):
        ''' Test internals doctests. '''

        run_module_test(denova.python.internals)

    def test_iter(self):
        ''' Test iter doctests. '''

        run_module_test(denova.python.iter)

    def test_log(self):
        ''' Test log doctests. '''

        run_module_test(denova.python.log)

    def test__log(self):
        ''' Test _log doctests. '''

        run_module_test(denova.python._log)

    def test_performance(self):
        ''' Test performance doctests. '''

        run_module_test(denova.python.performance)

    def test_text_file(self):
        ''' Test text_file doctests. '''

        run_module_test(denova.python.text_file)

    def test_times(self):
        ''' Test times doctests. '''

        run_module_test(denova.python.times)

    def test_utils(self):
        ''' Test python utils doctests. '''

        run_module_test(denova.python.utils)


if __name__ == "__main__":

    success = main()
    # exit with a system return code
    code = int(not success)
    sys.exit(code)

#!/usr/bin/env python3
'''
    Tests the doctests for denova.django_addons.

    The tests starting with xtest aren't being
    maintained so have been disabled.

    Copyright 2019-2022 DeNova
    Last modified: 2022-11-18
'''

import sys
from unittest import main, TestCase

import denova.django_addons.data_image
import denova.django_addons.singleton
import denova.django_addons.utils
import denova.django_addons.views

from denova.python.utils import run_module_test


class TestDoctests(TestCase):

    def test_data_image(self):
        ''' Test data_image doctests. '''

        run_module_test(denova.django_addons.data_image)

    def test_singleton(self):
        ''' Test singleton doctests. '''

        run_module_test(denova.django_addons.singleton)

    def test_utils(self):
        ''' Test django_addons utils doctests. '''

        run_module_test(denova.django_addons.utils)

    def test_views(self):
        ''' Test views doctests. '''

        run_module_test(denova.django_addons.views)


if __name__ == "__main__":

    success = main()
    # exit with a system return code
    code = int(not success)
    sys.exit(code)


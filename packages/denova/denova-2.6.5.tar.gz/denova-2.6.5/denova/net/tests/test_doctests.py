#!/usr/bin/env python3
'''
    Tests the doctests for denova.net.

    The tests starting with xtest aren't being
    maintained so have been disabled.

    Copyright 2019-2022 DeNova
    Last modified: 2022-11-18
'''

import os
import sys
from unittest import main, TestCase

import denova.net.browser
import denova.net.html_addons
import denova.net.http_addons
import denova.net.openssl
import denova.net.utils
import denova.net.web_log_parser

from denova.python.utils import run_module_test


class TestDoctests(TestCase):

    def test_browser(self):
        ''' Test browser doctests. '''

        run_module_test(denova.net.browser)

    def test_html_addons(self):
        ''' Test html_addons doctests. '''

        run_module_test(denova.net.html_addons)

    def test_http_addons(self):
        ''' Test http_addons doctests. '''

        run_module_test(denova.net.http_addons)

    def test_utils(self):
        ''' Test net utils doctests. '''

        run_module_test(denova.net.utils)

    def test_openssl(self):
        ''' Test openssl doctests. '''

        run_module_test(denova.net.openssl)

    def web_log_parser(self):
        ''' Test web_log_parser doctests. '''

        run_module_test(denova.net.web_log_parser)


if __name__ == "__main__":

    success = main()
    # exit with a system return code
    code = int(not success)
    sys.exit(code)

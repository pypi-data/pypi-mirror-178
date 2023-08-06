#!/usr/bin/env python3
'''
    Tests the doctests for denova.os.

    This is a unit test that includes doctests when we run unit tests.

    The tests starting with xtest aren't being
    maintained so have been disabled.

    Copyright 2019-2022 DeNova
    Last modified: 2022-11-18
'''

import os
import sys
from unittest import main, TestCase

import denova.os.cli
import denova.os.command
import denova.os.drive
import denova.os.fs
import denova.os.lock
import denova.os.osid
import denova.os.process
import denova.os.profile_addons
import denova.os.user

from denova.python.utils import run_module_test
from denova.tests.denova_test_case import DeNovaTestCase


class TestDoctests(TestCase):
    ''' Include doctests when we run unit tests. '''

    def test_cli(self):
        ''' Test cli doctests. '''

        run_module_test(denova.os.cli)

    def test_command(self):
        ''' Test command doctests. '''

        run_module_test(denova.os.command)

    def test_drive(self):
        ''' Test drive doctests. '''

        run_module_test(denova.os.drive)

    def test_fs(self):
        ''' Test fs doctests. '''

        run_module_test(denova.os.fs)

    def test_lock(self):
        ''' Test lock doctests. '''

        run_module_test(denova.os.lock)

    def test_osid(self):
        ''' Test osid doctests. '''

        run_module_test(denova.os.osid)

    def test_process(self):
        ''' Test process doctests. '''

        run_module_test(denova.os.process)

    def test_profile_addons(self):
        ''' Test profile_addons doctests. '''

        run_module_test(denova.os.profile_addons)

    def test_user(self):
        ''' Test user doctests. '''

        run_module_test(denova.os.user)


if __name__ == "__main__":

    success = main()
    # exit with a system return code
    code = int(not success)
    sys.exit(code)

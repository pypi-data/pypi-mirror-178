#!/usr/bin/env python3
'''
    Standard tests for testing test runners.

    Copyright 2022 DeNova
    Last modified: 2022-11-22
'''

from unittest import TestCase

class TestTests(TestCase):

    def test_success(self):
        '''
            Test that always succeeds.
        '''

        assert(True)

    def test_failure(self):
        '''
            Test that always fails.
        '''

        assert(False)

# -*- coding: utf-8 -*-

import os
import unittest
from square.configuration import Configuration
from square.client import Client


class ApiTestBase(unittest.TestCase):

    """All test classes inherit from this base class. It abstracts out
    common functionality and configuration variables set up."""

    @classmethod
    def setUpClass(cls):
        """Class method called once before running tests in a test class."""
        cls.request_timeout = 30
        cls.assert_precision = 0.01
        cls.config = ApiTestBase.create_configuration()
        cls.client = Client()

    @staticmethod
    def create_configuration():
        return Configuration(access_token=os.environ['SQUARE_SANDBOX_TOKEN'],
                             environment='sandbox')

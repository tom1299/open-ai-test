# Test case for the method getclass_signatures in class_data.py

import unittest
from class_data import getclass_help


# Define a class with a constructor and a method
class TestClass:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class GetClassHelpTest(unittest.TestCase):

    def test_getclass_help(self):
        """
        Test for the method getclass_signatures in class_data.py
        :return:
        """
        help_for_testclass = getclass_help(TestClass)
        print(help_for_testclass)
        assert "TestClass" in help_for_testclass

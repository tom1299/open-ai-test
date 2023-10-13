# Create a test case for the function in function_calling.py unsing unittest

import unittest
import openai

from function_calling import get_function_as_dict


class TestFunctionCalling(unittest.TestCase):
    """
    Test for the method get_function_as_dict in function_calling.py
    """
    def test_get_function_as_dict(self):
        function_as_dict = get_function_as_dict("get_balance")
        expected_parameters = {
            "type": "object",
            "properties": {
                "account_number": {
                    "type": "str"
                }
            },
            "required": ["account_number"]
        }
        self.assertEqual(function_as_dict["name"], "get_balance")
        self.assertIn("Return the balance of the account identified by the account number",
                      function_as_dict["description"])
        self.assertEqual(function_as_dict["parameters"], expected_parameters)

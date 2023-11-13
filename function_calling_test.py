# Create a test case for the function in function_calling.py unsing unittest
import unittest

from function_calling import get_function_as_dict, get_balance_with_prompt


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
                    "type": "string"
                }
            },
            "required": ["account_number"]
        }
        self.assertEqual(function_as_dict["name"], "get_balance")
        self.assertIn("Return the balance of the account identified by the account number",
                      function_as_dict["description"])
        self.assertEqual(function_as_dict["parameters"], expected_parameters)

    def test_get_balance_with_prompt(self):
        response = get_balance_with_prompt("My account number is A-1234 and I want to know my balance")
        self.assertIsNotNone(response)
        self.assertEqual(100, response)
        response = get_balance_with_prompt("Mon numéro de compte est A-1234 et je veux connaître mon solde")
        self.assertEqual(100, response)
        # Even works for Hebrew
        response = get_balance_with_prompt("מספר החשבון שלי הוא A-1234 ואני רוצה לדעת את היתרה שלי")
        self.assertEqual(100, response)
        try:
            get_balance_with_prompt("My social security number is A-1234 and I want to improve my work-life balance. How can I do that?")
        except Exception as e:
            self.assertIn("No function call found", str(e))

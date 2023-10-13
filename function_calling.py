# The following code contains a function that returns the current balance of a bank account
# The account is identified by the account number
# The account number is passed as an argument to the function
# Account numbers are strings in the format "A-1234" where A is a letter and 1234 are arbitrary digits
# Use a simple dictionary to store the account number and balance
# If the account number is not found add the account number with a balance of 0
# Return the balance

accounts = {"A-1234": 100.00, "B-1234": 200.00, "C-1234": 300.00}


def get_balance(account_number: str) -> float:
    """
    Return the balance of the account identified by the account number
    :param account_number: The account number
    :return: The balance of the account number
    """
    if account_number in accounts:
        return accounts[account_number]
    else:
        accounts[account_number] = 0
        return accounts[account_number]


# This python method is passed the name of a function and returns a dictionary representation of the function
# that can be used as a parameter to the openais function API
def get_function_as_dict(function_name: str):
    """
    Return a dictionary representation of the function that can be used as a parameter to the openais function API
    :param function_name: The name of the function
    :return: A dictionary representation of the function
    """
    import inspect
    function = globals()[function_name]
    function_signature = inspect.signature(function)
    # Create a dictionary of the function using inspect that adheres to the openai function API specification
    # https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions
    # Here is an example:
    #         {
    #             "name": "get_current_weather",
    #             "description": "Get the current weather in a given location",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "location": {
    #                         "type": "string",
    #                         "description": "The city and state, e.g. San Francisco, CA",
    #                     },
    #                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #                 },
    #                 "required": ["location"],
    #             },
    #         }
    function_signature_as_dict = {"name": function_name, "description": function.__doc__,
                                  "parameters": {"type": "object", "properties": {}, "required": []}}
    for parameter in function_signature.parameters:
        function_signature_as_dict["parameters"]["properties"][parameter] = {
            "type": function_signature.parameters[parameter].annotation.__name__ }
        function_signature_as_dict["parameters"]["required"].append(parameter)

    return function_signature_as_dict

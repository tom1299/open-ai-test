import openai

# The following code contains a function that returns the current balance of a bank account
# The account is identified by the account number
# The account number is passed as an argument to the function
# Account numbers are strings in the format "A-1234" where A is a letter and 1234 are arbitrary digits
# Use a simple dictionary to store the account number and balance
# If the account number is not found add the account number with a balance of 0
# Return the balance

accounts = {"A-1234": 100.00, "B-1234": 200.00, "C-1234": 300.00}

names_to_account_numbers = {"John Doe": "A-1234", "Jane Tarzan": "B-1234", "Jack Daniels": "C-1234"}


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


def get_account_numbers() -> list:
    """
    Return a list of account numbers
    :return: A list of account numbers
    """
    return list(accounts.keys())


def get_account_number(name: str) -> str:
    """
    Return the account number for a given name
    :param name: The name of the account holder
    :return: The account number
    """
    return names_to_account_numbers[name]


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
        parameter_type = function_signature.parameters[parameter].annotation.__name__
        # The following dict contains the mapping between python types and openai types
        # https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions
        type_mapping = {"str": "string", "float": "number", "int": "integer", "list": "array"}
        parameter_type = type_mapping[parameter_type]

        function_signature_as_dict["parameters"]["properties"][parameter] = {
            "type": parameter_type }
        function_signature_as_dict["parameters"]["required"].append(parameter)

    return function_signature_as_dict


# The following function calls openais completion API with the function as a parameter
# And a prompt that says "My account number is A-1234 and I want to know my balance"
def get_balance_with_prompt(prompt: str) -> int:
    """
    Return the balance of the account number in the prompt
    :param prompt: The prompt
    :return: The balance of the account number in the prompt
    """
    # Create two messages:
    # Role user: "My account number is A-1234 and I want to know my balance"
    # Role system: "Banking account program"
    messages = [{"role": "user", "content": prompt}, {"role": "system", "content": "Banking account program"}]

    # Create a list of functions
    functions = [get_function_as_dict(function_name) for function_name in globals() if callable(globals()[function_name])]

    # Pretty print the functions
    import json
    print(json.dumps(functions, indent=4))

    # Call the chat completion API using the model "gpt-3.5-turbo-instruct" passing the messages and functions
    # as parameters. Use the package openai

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions)["choices"][0]["message"]

    # Check if the response contains a function call
    # If so, call the function and return the result
    # If not, return the response
    if response.get("function_call"):
        function_name = response["function_call"]["name"]

        # Create a dictionary of functions in this module with the name as the key and the function as the value
        all_functions = {function.__name__: function for function in globals().values() if callable(function)}
        function_to_call = all_functions[function_name]
        function_args = json.loads(response["function_call"]["arguments"])

        # Given that function_args is a dictionary of arguments with the argument name as the key and the argument
        # value as the value, we can call the function using the ** operator
        return function_to_call(**function_args)
    else:
        raise Exception(f"No function call found in response for prompt: {prompt}")

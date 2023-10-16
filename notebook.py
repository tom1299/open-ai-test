import inspect


def get_address_as_string(name: str, age: int, address:dict) -> str:
    pass


def get_greeting(name: str) -> str:
    return f"Hello {name}"


if __name__ == '__main__':
    print (inspect.getsource(get_greeting))

    function_source = """
def get_greeting(name: str) -> str:
    return f"Hello {name}"
    """

    # Add the function to the module foo
    exec(function_source, globals())

    # Get the function from using a string as the name
    function = globals()["get_greeting"]
    # Call the function
    print(function("John"))

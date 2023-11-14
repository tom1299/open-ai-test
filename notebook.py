import inspect
import online_shop


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

method_source = """
def get_highest_priced_item(shop: online_shop.OnlineShop):
    stock = shop.get_stock()
    items = stock.get_items()
    
    highest_price = 0
    highest_priced_item = None
    
    for item in items.values():
        if item.get_price() > highest_price:
            highest_price = item.get_price()
            highest_priced_item = item
    
    return highest_priced_item
"""
exec(method_source, globals())
from class_data import getclass_help


def create_online_shop_prompt(classes: list, task_description: str):
    class_data = create_class_data(classes)
    prompt = f"""
    Context: Python programming, given the following classes in the module online_shop:
    ```txt
    {class_data}
    ```
    Task: Create a function that uses the classes above and takes a single parameter of type online_shop.OnlineShop and does the following: {task_description}. Only use classes from the module online_shopping. Do not include an example.
    """
    return prompt


def create_class_data(classes):
    class_data = ""
    for clazz in classes:
        class_help = getclass_help(clazz)
        class_data = class_data + class_help + "\n"
    class_data = class_data.encode('utf-8')
    return class_data



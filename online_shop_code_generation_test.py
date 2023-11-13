import copy
import json
import openai
import os
import re

import online_shop
from online_shop import Item, Stock, Order, Customer, OnlineShop
from online_shop_code_generation import create_online_shop_prompt
from online_shop_test import def_create_test_data


def extract_python_code(input_string):
    start_marker = "```python"
    end_marker = "```"
    start_index = input_string.find(start_marker)
    end_index = input_string.find(end_marker, start_index + len(start_marker))

    if start_index != -1 and end_index != -1:
        code_block = input_string[start_index + len(start_marker):end_index]
        return code_block.strip()  # Remove leading and trailing whitespace
    else:
        return None


def get_function_name(function_definition):
    pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
    match = re.match(pattern, function_definition)

    if match:
        return match.group(1)  # The first group captures the function name
    else:
        return None


openai.debug = True
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("context-template.json", "r") as file:
    context_template = json.load(file)

classes = [online_shop.Item, online_shop.Stock, online_shop.Order, online_shop.Customer, online_shop.OnlineShop]

online_shop = def_create_test_data()

tasks = ["Get the customer with the most orders", "Get the item with the highest price"]

for task in tasks:
    messages = copy.deepcopy(context_template)
    prompt = create_online_shop_prompt(classes, task)
    new_message = copy.deepcopy(messages[1])
    new_message["content"] = prompt

    messages.append(new_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    function_code = response["choices"][0]["message"]["content"]
    if "```python" in function_code:
        function_code = extract_python_code(response["choices"][0]["message"]["content"])

    print(function_code)
    function_name = get_function_name(function_code)

    # Add the function to this module
    exec(function_code, globals())

    globs = globals()

    # Get the function from using a string as the name
    function = globals()[function_name]

    result = function(online_shop)
    print(result)

    context_template.append({"role": "system", "content": function_code})
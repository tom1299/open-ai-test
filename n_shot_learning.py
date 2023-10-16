import inspect
import os
import openai
import logging

import http.client as http_client

if os.getenv("DEBUG"):
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

openai.debug = True
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use n shot learning to get more predictable results
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You will take python docstrings and convert them to python code"},
              {"role": "user", "content": """
              \"\"\"
              Say hello world
              \"\"\""""},
              {"role": "system", "content": "print(\"Hello, World!\")"},
              {"role": "user", "content": """
                \"\"\"
                Prints the numbers for 1 to 10
                \"\"\"
                """}
              ],
)

source_code = response["choices"][0]["message"]["content"]

# Some basic safeguards
# Note that executing arbitrary code generated by AI is dangerous
if len(source_code) > 50:
    raise Exception("Source code is too long")
elif not source_code.startswith("for i in"):
    raise Exception("Source code does not start with for i in")
elif not source_code.endswith("print(i)"):
    raise Exception("Source code does not end with print(i)")

print(f"Executing source code: \n{source_code}")

exec(source_code)
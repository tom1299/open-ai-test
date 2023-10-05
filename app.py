import os
import openai
import logging

# Activate request logging support.
# Caution: Might print the openai key to the console
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

openai.debug = True
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Say this is a test!",
    temperature=1,
    max_tokens=256
)

for choice in response["choices"]:
    print(choice["text"])
    print(choice["finish_reason"])
    print(choice["index"])

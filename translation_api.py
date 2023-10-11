# This file contains the translation of an english sentence to a the python programming language

import sys
import os
import openai
import logging

# Activate request logging support.
# Caution: Might print the openai key to the console
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

# List the available davinci engines
response = openai.Engine.list()
for engine in response["data"]:
    if "davinci" in engine["id"]:
        print(f"Engine: {engine['id']}")
        
def translate(textToTranslate, langSource="French", langTarget="English"):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Translate this from {langSource} into {langTarget} and the back again:\r\n{textToTranslate}",
        temperature=0.5,
        max_tokens=50
    )
    return response

sentences = ["Je m'appelle Jean"]

for sentence in sentences:
    response = translate(sentence)
    for choice in response["choices"]:
        print(f"Text: {choice['text']}")

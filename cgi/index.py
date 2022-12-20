#!/usr/bin/python

import os

method = os.environ["REQUEST_METHOD"]
script = os.environ["SCRIPT_FILENAME"]
query = os.environ["QUERY_STRING"]
if len(query) > 0:
    params = dict()
    for param in query.split('&'):
        param = param.split('=')
        params[param[0]] = param[1]

print("Content-Type: text/plain")
print()
print(f"Method: {method}")
print(f"Script: {script[script.rindex('/') + 1:]}")
if len(params):
    print(f"Query: {params}")

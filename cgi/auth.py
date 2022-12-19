#!/usr/bin/python

import os
import sys

content_length = 0

method = os.environ["REQUEST_METHOD"]

content_length += len(method) + 1

query = os.environ["QUERY_STRING"]

content_length += len(query) + 1

params = dict()
for param in query.split('&'):
    param = param.split('=')
    params[param[0]] = param[1]

content_length += len(str(params)) + 1

headers = {}
for k, v in os.environ.items():
    if k.startswith("HTTP_"):
        headers[k[5:].lower()] = v

k = "CONTENT_LENGTH"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]
k = "CONTENT_TYPE"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]

content_length += len(str(headers)) + 1

body = sys.stdin.read()

content_length += len(body)

print("Connection: close")
print(f"Content-Length: {content_length}")
print()
print(method)
print(query)
print(params)
print(headers)
print(body)
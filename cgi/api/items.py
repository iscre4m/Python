#!/usr/bin/python

import os
import mysql.connector
import configs
from dao import UserDAO

def send_401(message = None ):
    print("Status: 401 Unauthorized")
    print("WWW-Authenticate: Bearer realm 'Authorization required'")
    print()
    if message:
        print(message)
    return

    
if 'HTTP_AUTHORIZATION' in os.environ.keys():
    auth_header = os.environ['HTTP_AUTHORIZATION']
else:
    send_401("No token provided")
    exit()

if auth_header.startswith('Bearer'):
    token = auth_header[7:]
else:
    send_401("Authorization scheme Bearer required")
    exit()

try:
    connection = mysql.connector.connect(**configs.DB)
except mysql.connector.Error as error:
    send_401(error)
    exit()

user_dao = UserDAO(connection)
user = user_dao.read(token)[0]

if user is None:
    send_401("Token rejected")
    exit()

print("Status: 200 OK")
print("Content-Type: application/json;charset=UTF-8")
print()
print(f"'{user.username}'")
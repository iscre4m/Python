#!/usr/bin/python

import os
import base64
import mysql.connector
import configs
from datetime import datetime
from dao import UserDAO, AccessTokenDAO
import asyncio

def send_401(message = None):
    print("Status: 401 Unauthorized")
    if message:
        print("Content-Type: text/plain")
    print()
    if message:
        print(message)


async def connect():
    try:
        return mysql.connector.connect(**configs.DB)
    except mysql.connector.Error as error:
        send_401(error)
        exit()


async def main():
    db_connect = asyncio.create_task(connect())

    if 'HTTP_AUTHORIZATION' in os.environ.keys():
        auth_header = os.environ['HTTP_AUTHORIZATION']
    else:
        db_connect.cancel()
        send_401("No credentials provided")
        exit()

    if auth_header.startswith('Basic'):
        credentials = auth_header[6:]
    else:
        db_connect.cancel()
        send_401("Authorization scheme Basic required")
        exit()

    try:
        data = base64.b64decode(credentials, validate = True).decode('utf-8')
    except:
        db_connect.cancel()
        send_401("Invalid credentials: Base64 string required")
        exit()

    if not ':' in data:
        db_connect.cancel()
        send_401("Invalid credentials: login:password format expected")
        exit()

    login, password = data.split(':', maxsplit = 1)

    connection = await db_connect
    user = UserDAO(connection).read_by_credentials(login, password)

    if user is None:
        send_401("Credentials rejected")
        exit()
    
    access_token_dao = AccessTokenDAO(connection)
    access_token = access_token_dao.read_by_user_id(user.id)
    if access_token:
        token_expired = (access_token.expires - datetime.now()).seconds < 600
        if token_expired:
            access_token = access_token_dao.create(user)
    else:
        access_token = access_token_dao.create(user)

    if not access_token:
        send_401("Token creation error")
        exit()

    print("Status: 200 OK")
    print("Content-Type: application/json;charset=UTF-8")
    print()
    print(f"""{{
        'token':'{access_token.token}',
        'expires':'{access_token.expires}'
        'user_id':'{access_token.user_id}'
    }}""")

if __name__ == "__main__":
    asyncio.run(main())
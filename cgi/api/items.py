#!/usr/bin/python

import os

def send_401( message:str = None ) -> None :
    print( "Status: 401 Unauthorized" )
    print( 'WWW-Authenticate: Basic realm "Authorization required" ')
    print()
    if message :
        print( message )
    return
    
    
if 'HTTP_AUTHORIZATION' in os.environ.keys() :
    auth_header = os.environ['HTTP_AUTHORIZATION']
else :
    send_401()
    exit()

if auth_header.startswith( 'Basic' ) :
    credentials = auth_header[6:]
else :
    send_401( "Authorization scheme Basic required" )
    exit()
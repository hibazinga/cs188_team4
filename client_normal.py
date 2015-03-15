#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from time import sleep

s = socket.socket()         # Create a socket object
host = '192.168.1.39' # Get local machine name
port = 1180                # Reserve a port for your service.

s.connect((host, port))

data = 'Data received. Thank you.'
#s.send('Thank you for connecting')
while True:
    msg = s.recv(1024)
    print msg
    sleep(0.5)
    s.send(data)

s.close()                     # Close the socket when done

#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from time import sleep


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1180                   # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(1)                 # Now wait for client connection.


data = 'Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. Hello, this is a test message for CS188 course project. It is generated as a background traffic between legitimate users and clients. '


c, addr = s.accept()     # Establish connection with client.
c.settimeout(500)
print 'Got connection from', addr
c.send('Thank you for connecting')
while True:
    msg = c.recv(1024)
    print msg
    c.send(data)


c.close()                # Close the connection
s.close()

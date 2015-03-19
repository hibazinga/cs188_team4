6# server.py
import socket,sys
import time
import fcntl
from struct import *


# create a socket object
#serversocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

# get local machine name
#host = socket.gethostname()
#HOST = socket.gethostbyname(socket.gethostname())

serversocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#port = 9999

# bind to the port
#serversocket.bind((HOST, 80))

# Include IP headers
#serversocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
#fcntl.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# queue up to 5 requests
#threshold=5
#serversocket.listen()

log = open('data.log', 'w+')
log.write('--------------\n')
log.flush()



while True:
    # establish a connection
    #clientsocket,addr = serversocket.accept()
    #print("Got a connection from %s" % str(addr))
    #currentTime = time.ctime(time.time()) + "\r\n"
    #clientsocket.send(currentTime.encode('ascii'))
    
    packet = serversocket.recvfrom(65565)
    #print packet
    #packet string from tuple
    packet = packet[0]

    #take first 20 characters for the ip header
    ip_header = packet[0:20]
    
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
    
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    
    iph_length = ihl * 4
    
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    
    #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
    
    tcp_header = packet[iph_length:iph_length+20]
    
    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)
    
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
    syn=(tcph[5] >> 1 ) & 0x1
    ack=(tcph[5] >> 4 ) & 0x1
        #if dest_port!=80:
        #continue
        #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
    
    now = int(time.time()) #get current time
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    log.write('Time : ' +otherStyleTime + '\n')
    
    log.write('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr) + '\n')
    
    log.write('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length) + ' SYN : ' + str(syn) + ' ACK : ' + str(ack) +'\n')
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    
    #get data from the packet
    data = packet[h_size:]
    
    #print 'Data : ' + data
#print
    log.write('Data : ' + data + '\n')
    log.write('------------------------------------\n')

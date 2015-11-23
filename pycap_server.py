'''
Packet sniffer in python using the pcapy python library
 
Project website
http://oss.coresecurity.com/projects/pcapy.html
'''
 
import socket, sys
from struct import *
import time
import pcapy

import local_detection.main_olf as m

#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

def main(argv):
    
    log = open('data.log', 'w+')
    log.write('------------\n')
    log.flush()
    curtime = -1
    
    #list all devices
    devices = pcapy.findalldevs()
    print devices

    #ask user to enter device name to sniff
    print "Available devices are :"
    for d in devices :
        print d

    dev = raw_input("Enter device name to sniff : ")

    print "Sniffing device " + dev
    cap = pcapy.open_live(dev , 65536 , 1 , 0)

    #start sniffing packets
    while(1) :
        try:
            (header, packet) = cap.next()
        except Exception:
            continue
        #print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
        else:
            #parse_packet(packet)
                #parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_protocol = socket.ntohs(eth[2])
            #print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)
         
            #Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8 :
                #Parse IP header
                #take first 20 characters for the ip header
                ip_header = packet[eth_length:20+eth_length]
                 
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

                now = int(time.time()) #get current time
                timeArray = time.localtime(now)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                # on the fly
                if curtime == -1:
                    curtime = now
                else :
                    if now - curtime >= 5:
                        curtime = now
                        log.flush()
                        log.close()
                        m.run()
                        log = open('data.log', 'a+')

                log.write('Time : ' +otherStyleTime + '\n')
         
                log.write('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr) + '\n')
         
                #TCP protocol
                if protocol == 6 :
                    t = iph_length + eth_length
                    tcp_header = packet[t:t+20]
         
                    #now unpack them :)
                    tcph = unpack('!HHLLBBHHH' , tcp_header)
                     
                    source_port = tcph[0]
                    dest_port = tcph[1]
                    sequence = tcph[2]
                    acknowledgement = tcph[3]
                    doff_reserved = tcph[4]
                    tcph_length = doff_reserved >> 4
                    syn=(tcph[5] >> 1) & 0x1
                    ack=(tcph[5] >> 4) & 0x1
                     
                    log.write('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length) + ' SYN : ' + str(syn) + ' ACK : ' + str(ack) +'\n')
                     
                    h_size = eth_length + iph_length + tcph_length * 4
                    data_size = len(packet) - h_size
                     
                    #get data from the packet
                    data = packet[h_size:]

                    #print 'Data : ' + data

                    log.write('Data : ' + data + '\n')
                    log.write('------------------------------------\n')

if __name__ == "__main__":
  main(sys.argv)

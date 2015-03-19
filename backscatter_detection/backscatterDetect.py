import sys
import time
import math

# $ python backscatterDetect.py <filename>

r=sys.argv[1]
path_in = r

file=open(path_in, "r")
output=open("predict","w+")
threshold = 5 # sec
attack_threshold = 5000

line=file.readline()
mode=2
s=0
src_IP=""
dst_IP=""
src_port=""
dst_port=""
syn=0
ack=0
data_len=0
protocol=""
count=0 # number of implicit tcp connection request
dict={}
pkt_first=-1
pkt_last=-1
timecount=0
curpkt=0
curtime=-1
maxrate=-1.0

white_list=set([])

#after split:
#[Version, :, 4, IP, Header, Length, :, 5, TTL, :, 255, Protocol, :, 6, Source, Address, :, 93.83.82.209, Destination, Address, :, 192.168.3.145]
#[Source, Port, :, 39270, Dest, Port, :, 1180, Sequence, Number, :, 0, Acknowledgement, :, 0, TCP, header, length, :, 5, SYN, :, 1, ACK, :, 0]

while line:
    if line[0]!='-':
        print "data log format error - "
        print line
        break
    
    line=file.readline();
    if not line:
        break
    if line[0]=='T':   # Time : 2015-03-02 11:41:16
        tuple1 = time.strptime(line[7:26], "%Y-%m-%d %H:%M:%S");
        seconds = time.mktime(tuple1)
        if s==0:
            s=seconds
        if long(seconds)-s>=threshold:
            ## detection mechanism-2
            if mode==2:
                if curpkt/1.0>100:
                    timecount+=1
                maxrate=max(maxrate, curpkt/1.0)
               # print "Server is under DDoS Attack Mode 2!\n"
                print "Total SYN-Attack Packets: "+str(count)+" pkts\n"
                timeArray = time.localtime(pkt_first)
                print "Start time: "+ time.strftime("%Y-%m-%d %H:%M:%S", timeArray)+"\n"
                timeArray = time.localtime(long(seconds))
                print "End time: "+ time.strftime("%Y-%m-%d %H:%M:%S", timeArray)+"\n"
                print "Syn Packets: ", count, "\n"
                print "Attack Duration: "+str(timecount) + " seconds\n"
                print "Max Attack Rate: "+str(maxrate) + "\n"
                if count>=2500 and maxrate>=1000 and timecount>=3:
                    output.write(str(1)+'\n')
                    print "Server is under DDoS Attack!\n"
                else:
                    output.write(str(0)+'\n')
                    print "NO ATTACK!\n"

            ##
            s=seconds
            # print s
            # clear
            dict.clear()
            count=0
            pkt_first=-1
            pkt_last=-1
            curpkt=0
            curtime=-1
            maxrate=-1.0
            timecount=0
    
    else :
        print "data log format error Time"
        print line
        break
    
    line=file.readline();
    if line[0]=='V':   # Version : 4 IP Header Length : 5 TTL : 255 Protocol : 6 Source Address : 118.253.131.5 Destination Address : 192.168.3.145
        tmp = line.split(" ")
        protocol=tmp[13]
        src_IP=tmp[17]
        dst_IP=tmp[21]
    else :
        print "data log format error Version"
        break
    
    line=file.readline();
    if line[0]=='S':   # Source Port : 42709 Dest Port : 1180 Sequence Number : 0 Acknowledgement : 0 TCP header length : 5 SYN : 1 ACK : 0
        tmp = line.split(" ")
        src_port=tmp[3]
        dst_port=tmp[7]
        syn=int(tmp[22])
        ack=int(tmp[25])
    else :
        print "data log format error Source"
        break
    
    line=file.readline();
    if line[0]=='D':   # Data : ABCDEFGHIJKLMNOPQRSTUVWXYZ
        data_len=len(line)-6
    else :
        print "data log format error Data"
        break
    line=file.readline()
    while line=='\n' or (line not in '------------------------------------\n'):
        #print 'multi-line data'
        data_len+=len(line)
        line=file.readline()

    ## detect logic here
    if mode==1 :
        socket=src_IP
        socket+=dst_IP
        socket+=src_port
        socket+=dst_port
        
        if socket in white_list:
            continue
        if syn==0 :
            white_list.add(socket)
            continue
        
        if ack==1 :
            white_list.add(socket)
            continue
        if data_len > 900:
            white_list.add(socket)
            continue
        
        if pkt_first == -1:
            pkt_first = seconds
        pkt_last=seconds
        
        if socket not in dict:
            dict[socket] = 1
            count+=1
        else :
            if dict[socket]==1:
                count-=1
            dict[socket]=dict[socket]+1
        
        if count>= attack_threshold:
            print "Server is under DDoS Attack Mode 1!\n"
            print "Total SYN-Attack Packets: "+str(count)+" pkts\n"
            #print pkt_first
            timeArray = time.localtime(pkt_first)
            print "Start time: "+ time.strftime("%Y-%m-%d %H:%M:%S", timeArray)+"\n"
            timeArray = time.localtime(pkt_last)
            print "End time: "+ time.strftime("%Y-%m-%d %H:%M:%S", timeArray)+"\n"
            break
    
    elif mode==2 :
        socket=src_IP
        socket+=dst_IP
        socket+=src_port
        socket+=dst_port
        
        if socket in white_list:
            continue
        
        if syn==0 :
            white_list.add(socket)
            continue
        
        if ack==1 :
            white_list.add(socket)
            continue
        if socket not in dict:
            dict[socket] = 1
            count+=1
            curpkt+=1
        '''
        else :
            if dict[socket]==1:
                count-=1
                curpkt-=1
                dict[socket]=dict[socket]+1
        '''
        '''
        if syn==1 and ack==0 and socket not in dict:
            count+=1
            curpkt+=1
            dict[socket] = 1
        '''
        if pkt_first == -1:
            pkt_first = seconds
            curtime = seconds
        pkt_last=seconds
        if pkt_last - curtime>=1:
            curtime = pkt_last
            if curpkt/1.0 > 100:
                timecount+=1
            maxrate=max(maxrate, curpkt/1.0)
            curpkt=0
    
    elif mode==3:
        if int(src_IP[len(src_IP)-1])%2 == 1:
            continue
        socket=src_IP
        socket+=dst_IP
        socket+=src_port
        socket+=dst_port
        
        if socket in white_list:
            continue
        if syn==0 :
            white_list.add(socket)
            continue
        
        if ack==1 :
            white_list.add(socket)
            continue
        if data_len > 900:
            white_list.add(socket)
            continue
        if pkt_first == -1:
            pkt_first = seconds
        pkt_last=seconds
        
        if socket not in dict:
            dict[socket] = 1
            count+=1
        else :
            if dict[socket]==1:
                count-=1
            dict[socket]=dict[socket]+1
        
        if count>= attack_threshold/2:
            print "Server is under DDoS Attack Mode 3!\n"
            print "Total SYN-Attack Packets: "+str(count)+" pkts\n"
            print "Start time: "+ time.strftime("%Y-%m-%d %H:%M:%S", pkt_first)+"\n"
            print "End time: "+ time.strftime("%Y-%m-%d %H:%M:%S", pkt_last)+"\n"
            break
    
    ##

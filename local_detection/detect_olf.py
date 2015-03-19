import sys
import time

def det(last_pos, n_time):
    #r=sys.argv[1]
    path_in = "./data.log" 
    print "calling detection ", n_time, " time", "print position", last_pos
    file=open(path_in, "r")
    
    file.seek(last_pos) #seek the write position of writing
    
    #for each macro-flow 
    #number of distinct source ip
    #number of source ip
    
   
    #for each micro-flow(four features same) 
    #average size = total size/number of packets
    #number of source ip and source port(this changes quickly during attacking)
    
    attack_duration = 5 # detect every 10 sec
    
    total_entry = 0 # total number of entries during this reading file
    flow_num = 0 #total number of flow
    label_num = 0    
    macro_num = 0 #number of macro flow: number of packets in any time interval
    micro_num = 0 #number of micro flow: flow with the same four features
    third_shake_num = 0
    
    #attack_threshold = 500  This value is to be computed
    packet_rate = 1 #compute the packet rate of each flow
    
    label = 0
    thresh = 0.2

    if n_time == 1:
    	line=file.readline();
    else:
    	line="123"
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
    micro_set = set([]) # holding all micro_flow in a certain time interval
    src_add = set([])
    labels = []
    data_size = 0
    
    result = []

    #after split:        
    #[Version, :, 4, IP, Header, Length, :, 5, TTL, :, 255, Protocol, :, 6, Source, Address, :, 93.83.82.209, Destination, Address, :, 192.168.3.145]
    #[Source, Port, :, 39270, Dest, Port, :, 1180, Sequence, Number, :, 0, Acknowledgement, :, 0, TCP, header, length, :, 5, SYN, :, 1, ACK, :, 0]

    while line:
        if line[0]!='-':
            print "data log format error",
    
        line=file.readline();
        #print line
        if not line:
            break
        if line[0]=='T':   # Time : 2015-03-02 11:41:16
            tuple1 = time.strptime(line[7:26], "%Y-%m-%d %H:%M:%S");
            seconds = time.mktime(tuple1)
            if s==0 or long(seconds)-s>=attack_duration:
                #display the information
                if s!= 0:
                    temp_res  = []
                    #print "For flow ", flow_num
                    #temp_res.append(flow_num)
                    #print "macro flow number : ", macro_num    
                    temp_res.append(macro_num)
                    #print "micro flow number: ", len(micro_set)
                    temp_res.append(len(micro_set))
                    packet_rate = macro_num * 1.0 /attack_duration
                    #print "packet rate " , packet_rate
                    temp_res.append(packet_rate)
                    #print "distinct source address ", len(src_add)
                    temp_res.append(len(src_add))
                    #print "average packet(data) length ", data_size
                    temp_res.append(data_size)
                    #print "number of third step of shaking", third_shake_num
                    judge = 0
                    if label_num > thresh * macro_num:
                        judge = 1
                    #if judge == 1:
                     
                    #print "label of the flows", judge
                    labels.append(judge)
                    #print "------------------------------------------"
                    
                    result.append(temp_res)
                    flow_num += 1
                    last_pos = file.tell()
                    file.close()
                    return last_pos, result,labels

        #            print flow_num
                # do all the computation here
                
                # update of parameters
                s=seconds
                macro_num = 0
                label_num = 0
                micro_set.clear()
                src_add.clear()
                count=0
                data_size = 0
                third_shake_num = 0
        else :
            print "data log format error 1:",line
        
        line=file.readline();
        if line[0]=='V':   # Version : 4 IP Header Length : 5 TTL : 255 Protocol : 6 Source Address : 118.253.131.5 Destination Address : 192.168.3.145
            tmp = line.split(" ")
            protocol=tmp[13]
            src_IP=tmp[17]
            dst_IP=tmp[21]
        else :
            print "data log format error 2",line
        
        line=file.readline();
        if line[0]=='S':   # Source Port : 42709 Dest Port : 1180 Sequence Number : 0 Acknowledgement : 0 TCP header length : 5 SYN : 1 ACK : 0
            tmp = line.split(" ")
            src_port=tmp[3]
            dst_port=tmp[7]
            src_address = src_IP
            src_address += src_port
            src_add.add(src_address)
            #dst_ports.add(dst_port)
            syn=int(tmp[22])
            ack=int(tmp[25])
            
        else :
            print "data log format error 3",line

        line=file.readline();
        if line[0]=='D':   # Data : ABCDEFGHIJKLMNOPQRSTUVWXYZ
            data_len=len(line)-6
            tmp = line.split(' ')
            
            if "ABCDEFGHIJKLMNOPQRSTUVWXYZ" in tmp[2]:
                label_num = label_num + 1
                #print label_num
        else :
            print "data log format error 4",line
        
        line=file.readline()
        while line[0]== '\n' or line not in '--------------------------------------\n':
            data_len+=len(line)
            line=file.readline()
        
        data_size += data_len
        ## detect logic here
        
        socket=src_IP
        socket+=dst_IP
        socket+=src_port
        socket+=dst_port
        micro_set.add(socket)
      
        total_entry = total_entry + 1
        macro_num = macro_num + 1
        #print flow_num
        #line=file.readline();
        #read the extra line here
        
    
   
    #Average Number of Packets in Per Flow(ANPPF).
    sum = 0
    
    print "Information for this reading: "
    print "Total Packets :" ,total_entry
    flow_num = flow_num-1
    print "Total flows :", flow_num 


    temp_res  = []
    #print "For flow ", flow_num
    #temp_res.append(flow_num)
    #print "macro flow number : ", macro_num    
    temp_res.append(macro_num)
    #print "micro flow number: ", len(micro_set)
    temp_res.append(len(micro_set))
    packet_rate = macro_num * 1.0 /attack_duration
    #print "packet rate " , packet_rate
    temp_res.append(packet_rate)
    #print "distinct source address ", len(src_add)
    temp_res.append(len(src_add))
    #print "average packet(data) length ", data_size
    temp_res.append(data_size)
    #print "number of third step of shaking", third_shake_num
    judge = 0
    if label_num > thresh * macro_num:
        judge = 1
    #if judge == 1:
     
    #print "label of the flows", judge
    labels.append(judge)
    #print "------------------------------------------"
    
    result.append(temp_res)








     
    print len(result)
    print len(labels)



    last_pos = file.tell()
	print "last_pos", last_pos
    file.close()    
    return last_pos, result,labels

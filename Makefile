CC=g++
CFLAGS = -g 
# uncomment this for SunOS
# LIBS = -lsocket -lnsl

all: Bot1 Bot2 BotM

Bot1: Bot1.o 
	$(CC) -o Bot1 Bot1.o $(LIBS)

Bot2: Bot2.o 
	$(CC) -o Bot2 Bot2.o $(LIBS)

BotM: BotM.o 
	$(CC) -o BotM BotM.o $(LIBS)

Bot1.o: Bot1.cpp

Bot2.o: Bot2.cpp

BotM.o: BotM.cpp

clean:
	rm -f Bot1 BotM Bot2 Bot1.o Bot2.o BotM.o 

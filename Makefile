CC=g++
CFLAGS = -g 
# uncomment this for SunOS
# LIBS = -lsocket -lnsl

all: Bot BotM

Bot: Bot.o 
	$(CC) -o Bot Bot.o $(LIBS) 

BotM: BotM.o 
	$(CC) -o BotM BotM.o $(LIBS)

Bot.o: Bot.cpp BotProtocol.h

BotM.o: BotM.cpp BotProtocol.h

clean:
	rm -f Bot BotM Bot.o BotM.o 

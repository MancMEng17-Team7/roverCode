#ifndef roverComs_h
#define roverComs_h

#include "Arduino.h"

typedef struct comMsg {
	int id;						// Message ID: counter to identify replys.
	int size;					// Size of message in bytes.
	char* ptr;					// Pointer to data in message.
} comMsg;

class roverComs
{
	public:
		roverComs();
		void sendMsg(comMsg* msg);
		comMsg getMsg();
	private:
};

#endif
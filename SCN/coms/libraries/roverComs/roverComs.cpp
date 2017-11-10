#include "Arduino.h"
#include "roverComs.h"
#include <cmath>

roverComs::roverComs()
{
	Serial.begin(9600);
}

void roverComs::sendMsg(comMsg* msg)
{
	Serial.print('<');
	
	char str_id[10];
	itoa(msg->id, (char *)&str_id, 10);
	
	for (int i = 0; str_id[i] != NULL; i++)
	{
		Serial.print(str_id[i]);
	}
	
	Serial.print(':');
	
	for (char i; i < msg->size; i++)
	{
		Serial.print(msg->ptr[i]);
	}
	
	Serial.print('>');
}

comMsg roverComs::getMsg()
{	
	comMsg new_msg;
	
	char buf[100];
	char size = 0;
	
	new_msg.size = 0;
	new_msg.ptr = (char*)malloc(100);
	
	do
	{
		for (char i = 0; Serial.available() > 0; i++)
		{		
			buf[i] = Serial.read();
			size = i + 1;
		}
		
		if (buf[size - 1] == '>')
		{
			break;
		}
	} while (size != 0);
	
	char msg_start = 0;
	for (char i = 0; i < size; i++)
	{
		if (buf[i] == ':')
		{
			msg_start = i + 1;
			break;
		}
	}
	
	new_msg.size = size - 1 - msg_start;
	new_msg.ptr = (char *)realloc(new_msg.ptr, new_msg.size);
	new_msg.id = 0;
	for (char i = 0; i < size - 1; i++)
	{
		new_msg.ptr[i] = buf[msg_start + i];
	}
	for (char i = 0; i < msg_start - 2; i++)
	{
		new_msg.id += pow(10, i) * (buf[msg_start - 2 - i] - '0');
	}
	
	return new_msg;
}
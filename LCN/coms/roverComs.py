#============================================================================================
# MODULE IMPORTS:
#============================================================================================
import time
import serial
from USBUtils import *

#============================================================================================
# FUNCTION DEFINITIONS:
#============================================================================================
#--------------------------------------------------------------------------------------------
def getSubNodes():
#--------------------------------------------------------------------------------------------
# Returns a dictionary of connected nodes and their device mount points.
	con_nodes = {}
	con_devs = getUSBDevices()

	for mnt,info in con_devs.iteritems():
		if info[2].lower() == "teensyduino":
			con_nodes[mnt] = info

	return con_nodes
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def initComs(nodes):
#--------------------------------------------------------------------------------------------
# Initialises communication channels with each node passed. Returns new dictionary of nodes
# containing serial objects.
	if len(nodes) <= 0:
		print "ERROR: No nodes in list!"
		return

	for mnt,info in nodes.iteritems():
		mnt_path = "/".join(["/dev", mnt])
		print "Connecting to node at", mnt_path
		serial_port = serial.Serial(port=mnt_path, baudrate=9600, timeout=5)
		info.append(serial_port)
		nodes[mnt] = info

	return nodes
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def sendMsg(node, msg):
#--------------------------------------------------------------------------------------------
# Sends a message to node.
	node_info = node.values()[0]
	sendMsg.msgCounter += 1
	packet = "".join(['<', str(sendMsg.msgCounter), ':', msg, '>'])
	node_info[3].write(packet)
	node_info[3].flush()
	return sendMsg.msgCounter
sendMsg.msgCounter = 0;
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def getMsg(node):
#--------------------------------------------------------------------------------------------
# Checks and gets message from node.
	node_info = node.values()[0]
	packet = [node_info[3].read()]

	if packet[0] != '<':
		print "ERROR: Packets out of sync!"
		print "".join(["	Recieved '", packet[0], "' as starting character"])
		return 0,""
	while 1:
		packet.append(node_info[3].read())
		if packet[-1] == '>':
			break

	packet = "".join(packet[1:-1])
	packet = packet.split(':')

	return packet[0], packet[1]
#--------------------------------------------------------------------------------------------

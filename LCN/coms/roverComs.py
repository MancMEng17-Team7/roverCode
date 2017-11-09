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
	con_nodes = []
	con_devs = getUSBDevices()

	for dev in con_devs:
		if dev['dev_man'].lower() == "teensyduino":
			con_nodes.append(dev)

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

	for x,node in enumerate(nodes):
		mnt_path = "/".join(["/dev", node['dev_mnt']])
		print "Connecting to node at", mnt_path
		serial_port = serial.Serial(port=mnt_path, baudrate=9600, timeout=5)
		nodes[x]['port'] = serial_port
		return nodes
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def sendMsg(node, msg):
#--------------------------------------------------------------------------------------------
# Sends a message to node.
	sendMsg.msgCounter += 1
	packet = "".join(['<', str(sendMsg.msgCounter), ':', msg, '>'])
	node['port'].write(packet)
	return sendMsg.msgCounter
sendMsg.msgCounter = 0;
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
def getMsg(node):
#--------------------------------------------------------------------------------------------
# Checks and gets message from node.
	packet = [node['port'].read()]
	if packet[0] != '<':
		print "ERROR: Packets out of sync!"

	while 1:
		packet.append(node['port'].read())
		if packet[-1] == '>':
			break

	packet = "".join(packet[1:-1])
	packet = packet.split(':')

	return packet[0], packet[1]
#--------------------------------------------------------------------------------------------

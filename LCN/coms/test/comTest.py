import sys
import time
sys.path.insert(0, '../')

from roverComs import *

nodes = getSubNodes()
initComs(nodes)

print "Beginning Test:"

x = 0
while x <= 100:
	msg = " ".join(["Message", str(x)])
	msg_num = sendMsg(nodes[0], msg)
	print "".join(["Sent (", str(msg_num),")'", msg, "'"])

	ret_num,ret_msg = getMsg(nodes[0])
	print "".join(["Recieved (", str(ret_num),")'", ret_msg, "'"])

	if ret_msg != str(msg):
		print "FAILED:", ret_msg, "!=", msg
		break
	else:
		print "Success:", ret_msg, "==", msg
	print ""

	x = x + 1

nodes[0]['port'].close

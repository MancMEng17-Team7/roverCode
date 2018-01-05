import sys
import time
sys.path.insert(0, '../')

from roverComs import *

num_iter = int(raw_input("Number of Iterations: "))

failed = 0
cur_iter = 1

while cur_iter <= num_iter:
	print " ".join(["Running Iteration", str(cur_iter), "============================================================"])

	nodes = getSubNodes()
	initComs(nodes)

	print "Beginning Test:"

	num_devs = len(nodes.keys())
	print " ".join(["Num. Nodes =", str(num_devs)])

	dev_num = 0
	while dev_num < num_devs:
		target_node = {nodes.keys()[dev_num] : nodes.values()[dev_num]}

		print " ".join(["\nTesting node:", target_node.keys()[0], "-------------------------------------"])

		x = 0
		while x <= 20:
			#msg = " ".join(["Message", str(x)])
			msg = "speed=10"
			msg_num = sendMsg(target_node, msg)
			print "".join(["Sent (", str(msg_num),")'", msg, "'"])

			print target_node.values()[0][3].in_waiting

			ret_num,ret_msg = getMsg(target_node)
			print "".join(["Recieved (", str(ret_num),")'", ret_msg, "'"])

			if ret_msg == "":
				failed = 1;
				print "FAILED: No message recieved before timeout."
				break

			if ret_msg != str(msg):
				failed = 1
				print "FAILED:", ret_msg, "!=", msg
				break
			else:
				print "Success:", ret_msg, "==", msg
			print ""

			x = x + 1

		dev_num = dev_num + 1

	for mnt,info in nodes.iteritems():
		print " ".join(["Closing Coms link to", mnt])
		info[3].close()

	cur_iter = cur_iter + 1

if failed == 1:
	print
	print "TEST FAILED"
else:
	print
	print "TEST PASSED"

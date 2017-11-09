from subprocess import Popen, PIPE

def getUSBDevices():
	devices = []

	p1 = Popen(['dmesg', ''], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	p2 = Popen(['grep', '-i', 'usb'], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
	output, err = p2.communicate()

	lines = output.splitlines()

	i = 0;
	while i < len(lines):
		line = lines[i]

		if line[15:18] == "usb" :

		# Scan "dmesg" output for USB connections...
			if line[24:27] == "new":

				# Get device Number...
				dev_num = line[57:].split(" ", 1)[0]
				#print(dev_num)

				# Get device Product...
				i = i + 3
				line = lines[i]
				dev_pro = line[15:].split(" ", 3)[3:][0]
				#print(dev_pro)

				# Get device Manufacturer...
				i = i + 1
				line = lines[i]
				dev_man = line[15:].split(" ", 3)[3:][0]
				#print(dev_man)

				# Get devices mount point...
				i = i + 2
				line = lines[i]
				dev_mnt = line[15:].split(" ")[2][:-1]
				#print(dev_mnt)

				#dev_info = [dev_num, dev_pro, dev_man]
				#devices[dev_mnt] = dev_info

				devices.append({'dev_mnt' : dev_mnt, 'dev_num' : dev_num, 'dev_man' : dev_man})

				# Scan "dmesg" output for USB Disconnects...
			if line[24:38] == "USB disconnect":
				dis_num = line[15:].split(" ")[6]
				#for mount,info in devices.items():
				#	if info[0] == dis_num:
				#		devices.pop(mount)
				for x,dev in enumerate(devices):
					if dev['dev_num'] == dis_num:
						del devices[x]

		i = i + 1

	return devices

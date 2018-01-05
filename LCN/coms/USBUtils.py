from subprocess import Popen, PIPE

def getUSBDevices():
	devices = {}

	p = Popen(['dmesg', ''], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate()

	lines = output.splitlines()

	i = 0;
	while i < len(lines):
		line = lines[i]

		if line[15:18] == "usb" :

			#DIRTY HACK TO MAKE USB HUB WORK
			off = 2

		# Scan "dmesg" output for USB connections...
			if line[24+off:27+off] == "new":

				dev_num = ""
				dev_pro = ""
				dev_man = ""
				dev_mnt = ""

				# Get device Number...
				dev_num = line[57+off:].split(" ", 1)[0]
				#print(dev_num)

				# Get device Product...
				i = i + 3
				line = lines[i]
				dev_pro = line[15:].split(" ", 3)[3:][0]
				#print(dev_pro)

				if dev_pro != "USB2.0 Hub":

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

				dev_info = [dev_num, dev_pro, dev_man]
				devices[dev_mnt] = dev_info

				# Scan "dmesg" output for USB Disconnects...
			if line[24+off:38+off] == "USB disconnect":
				dis_num = line[15:].split(" ")[6]
				for mount,info in devices.items():
					if info[0] == dis_num:
						devices.pop(mount)

		i = i + 1

	return devices

import sys,re
from subprocess import Popen, PIPE

import matplotlib.pyplot as plt

cmd = "ping riot.de -t"

proc = Popen(cmd, shell=True, bufsize=1, stdout=PIPE, universal_newlines = True)

res_regexp = re.compile(r'=(\d+) ms')

i = 0
x_values = []
ping_values = []


for line in iter(proc.stdout.readline,''):
	i += 1

	## Get ping from server

	ping = res_regexp.search(line)
	ms = 0
	if(ping):
		ms = int(ping.group(1))
		x_values.append(i)
		ping_values.append(ms)
	elif(line.find("D") != -1):
		ms = 999
		x_values.append(i)
		ping_values.append(ms)
	else:
		print(line[0:5])
	print("ms : "+str(ms))

	## Show the data
	plt.plot(x_values,ping_values)
	plt.draw()

	plt.pause(0.1)


proc.stdout.close()
proc.wait()
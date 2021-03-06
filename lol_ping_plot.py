import sys,re
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt

servers = {"NA":"104.160.131.3","EUW":"104.160.141.3","EUNE":"104.160.142.3","OCE":"104.160.156.1","LAN":"104.160.136.3"}

def print_help():
	print('Usage: py lol_ping_plot.py [server]/[custom [server_ip]] - plot server ping')
	print('Supported servers: EUW, NA, EUNE, OCE, LAN')
## Get server name as command line argument

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print_help()
	sys.exit()

server_ip = ""

if(sys.argv[1].upper() == "CUSTOM"):
	if(len(sys.argv) != 3):
		print_help()
		sys.exit()
	server_ip = sys.argv[2]
else:
	server_name = sys.argv[1].upper()
	server_ip = servers[server_name]

cmd = "ping "+server_ip+" -t"

## Start probing for latency

proc = Popen(cmd, shell=True, bufsize=1, stdout=PIPE, universal_newlines = True)

res_regexp = re.compile(r'=(\d+) ms')


request_num = 0
x_values = []
ping_values = []


for line in iter(proc.stdout.readline,''):
	request_num += 1

	## Get ping from server

	ping = res_regexp.search(line)
	ms = 0
	if(ping): # Got ping correctly
		ms = int(ping.group(1))
		x_values.append(request_num)
		ping_values.append(ms)
	else: # Can't get response / packet loss
		ms = 999
		x_values.append(request_num)
		ping_values.append(ms)

	## Show the data
	plt.plot(x_values,ping_values)
	plt.draw()

	plt.pause(0.1)


proc.stdout.close()
proc.wait()
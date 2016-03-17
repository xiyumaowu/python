#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import optparse
import time
from socket import *
from threading import *

screenLock = Semaphore(value = 1)
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print('[+] %d/tcp open' % tgtPort)
#        print('[+]' + str(results))
    except Exception as e:
    	screenLock.acquire()
    	pass
    	# print('[-] %d /tcp closed' % tgtPort)
    finally:
    	screenLock.release()
    	connSkt.close()

def portScan(tgtHost, tgtPorts):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print("[-] Cannot resolve '%s' : Unknown host" % tgtHost)
		return
	try:
		tgtName = gethostbyaddr(tgtIP)
		print('\n[+] Scan Results for: ' + tgtName[0])
	except:
		print('\n[+] Scan Results for: ' + tgtIP)
	setdefaulttimeout(1)

	for tgtPort in range(1,99999):
		t = Thread(target = connScan, args = (tgtHost, int(tgtPort)))
		try:
			t.start()
			if tgtPort%1000 == 0 :
				time.sleep(0.5)		
		except Exception as e:
			print("[-] the Max Thread Number is: " + str(tgtPort))
			return

def main():
	parser = optparse.OptionParser('usage%prog -H <target host> -p <target port>')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify target host')
	parser.add_option('-P', dest = 'tgtPort', type = 'string', help = 'specify target port[s] separated by comma')
	(options, args) = parser.parse_args()

	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(',')

	if (tgtHost == None) | (tgtPorts[0] == None):
		print (parser.usage)
		exit(0)

	portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
	main()
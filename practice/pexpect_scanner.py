#! /usr/bin/python3
# _*_ coding:utf-8 _*_


__author__ = 'Junliang.Zhong'

import pexpect

PROMPT = ['#', '>>>', '>', ',', '\$']

def send_command(child, cmd):
	try:
		child.sendline(cmd)
		child.expect(PROMPT)
		print (child.after)
	except Exception as e:
		print('connecting failed!')

def connect(user, host, password):
	ssh_newkey = 'Are you sure to continue connecting?'
	connStr = 'ssh ' + user + '@' + host 
	child = pexpect.spawn(connStr)

	ret = child.expect([pexpect.TIMEOUT, 'password:'])
	if ret == 0 :
		print('[-] Error Connecting')
		return
	child.sendline(password)
	child.expect(PROMPT)
	return child

def main():
 	host = 'localhost'
 	user = 'ezhonju'
 	password = 'Eric2019'
 	child = connect(user, host, password)
 	send_command(child, 'll')

if __name__ == '__main__':
	main()
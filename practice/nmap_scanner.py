#! /usr/bin/python3
# _*_ coding:utf-8 _*_


__author__ = 'Junliang.Zhong'

import nmap
import optparse

def nmapScan(tgtHost, tgtPort):
	try:
		nmScan = nmap.PortScanner()
		nmScan.scan(tgtHost, tgtPort)
		state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
		print('[*]' + tgtHost + 'tcp/' + tgtPort +' ' + state)
	except Exception as e:
		print(e)

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

	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
	main()
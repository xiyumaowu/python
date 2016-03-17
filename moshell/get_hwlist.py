#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'

import os
from threading import *
import datetime
_Ex_str = ''

def logon(ip):
	fn = str(ip)
	try:
		if ip != '':
			os.system('moshell %s "run moshell_command.mos" >> %s' % (ip,fn))
			return (True, fn)
		else:
			pass
	except Exception as e:
		return (False, fn)

def print_hw(ip):
	(login,fn) = logon(ip)
	global _Ex_str
	_Ex_str += str(ip) + ":\r\n"
	if login:
		_f = open(fn)
		_all_lines = _f.readlines()
		_f.close()
		os.system('rm %s' %fn)
		_line_count = 0
		_line_len = len(_all_lines)

		while _line_count < _line_len:
			_str = _all_lines[_line_count]
			if 'DUS' in _str or 'RRU' in _str:
				_Ex_str += _str
			_line_count += 1

def main():
	global _Ex_str
	start_t = datetime.datetime.now()
	print('start time: %s' % start_t )
	
	ip_f = open('eNB_iplist')
	ip_list = ip_f.readlines()
	for ip in ip_list:
		ip = ip.strip('\r').strip('\n')
		if ip != '':
			try:
				t = Thread(target = print_hw, args = (ip,))
				t.start()
				t.join()
			except Exception as e:
				print(e)
		else:
			pass
	print(_Ex_str)
	
	end_t = datetime.datetime.now()
	print('end time: ' + end_t)
	print('the process remaining time: %s s' %(end_t - start_t))


if __name__ == '__main__':
	main()
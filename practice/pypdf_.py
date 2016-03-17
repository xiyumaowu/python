#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'

import pyPdf
import optparse
from pyPdf import PdfFileReader

def printMeta(filename):
	pdfile = PdfFileReader(file(filename, 'rb'))
	docInfo = pdfile.getDocumentInfo()
	print('[*] PDF MetaData For: ' + str(filename))
	for metaItem in docInfo:
		print('[+] ' + metaItem + ":" + docInfo[metaItem])

def main():
	parser = optparse.OptionParser('usage%prog  -F <PDF filename>')
	parser.add_option('-F', dest = 'filename', type = 'string', help = 'specific the PDF file name')
	(options, args) = parser.parse_args()
	filename = options.filename

	if filename == None:
		print(parser.usage)
		exit(0)
	else:
		printMeta(filename)

if __name__ == '__main__':
	main()
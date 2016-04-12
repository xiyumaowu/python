#! /usr/bin/python3
# _*_ coding:utf-8 _*_


__author__ = 'Junliang.Zhong'

from django.http import HttpResponse
from django.shortcuts import *
from Radio.get_hwlist import *



def index(req):
	if req.method == 'POST':
		return render_to_response('index.html',{'title':get_Ex_str(), 'user':'ezhonju'})
		
	else:
		pass

	iplist = get_eNB_ip('eNB_iplist')
	return render_to_response('first.html',{'iplist':iplist})

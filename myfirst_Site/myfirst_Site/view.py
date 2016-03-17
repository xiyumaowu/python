#! /usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Junliang.Zhong'

from django.http import HttpResponse
from django.shortcuts import *

def hello(request):
	return render_to_response('first.html')
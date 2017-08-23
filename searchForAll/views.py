# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

import datetime
import os
from crawler import mainprocess
from proxyManager import storeProxy

def hello(request):
    context = {}
    context['hello'] = 'Hello World! meng'
    return render(request, 'hello.html', context)

def search(request):
    context = {}
    context['hello'] = 'Hello World! meng'
    return render(request, 'search.html', context)

def searchResult(request):
	keyword=request.GET['kw']
	page = request.GET.get('page',1)
	type = request.GET.get('type',0)

	urlinfos=[]
	urlinfos=mainprocess.keywordSearch(keyword,page,type)
	#urlinfo1={"url":"http://www.baidu.com/link?url=966OdUyxuwFJoAYx_XGYq7_FiVLcej4qEA3Q84e-lLAtLPRGGHA6tsNFNsTN9zka&wd=&eqid=a64931cc000026c3000000035994fd9e","title":"python Django教程 之模板渲染、循环、条件判断、常用的..._博客园","info":'在 W3School,您将找到许多可以在线编辑并测试的 jQuery 实例。 jQuery 实例jQuery 参考手册 在W3School,您将找到包含所有 jQuery 对象和函数的完整参考手册。 jQuery...'}
	#urlinfos.append(urlinfo1)
	list=[i+1 for i in range(8)]
	context = {}
	context['urlinfos'] = urlinfos
	context['pagenums'] = list
	#print urlinfos

	return render(request, 'searchResult.html', context)


def addproxy(request):#传入代理的分隔符设置为 ‘;’  curl 'http://localhost:8000/addproxy' -d 'proxy=192.168.200.252:3127%3B192.168.222%3B5555'
	proxyContent = request.POST.get('proxy')
	proxys=proxyContent.split(';')
	storeProxy.store(proxys)
	return HttpResponse('ok')
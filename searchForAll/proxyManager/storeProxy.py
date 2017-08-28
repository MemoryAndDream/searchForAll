#coding=utf8
import fcntl
import os
import os,sys
import json
import urllib2
import cookielib
import ConfigParser
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode


proxyFilePath='proxy.txt'
import time

def store(proxys):
	pidfile = open(proxyFilePath, "a")
	for i in range(10):
		try:
			fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)  # LOCK_EX 排他锁:除加锁进程外其他进程没有对已加锁文件读写访问权限
			# LOCK_NB 非阻塞锁: 如果指定此参数，函数不能获得文件锁就立即返回，否则，函数会等待获得文件锁。
			if type(proxys) == type([]):
				for proxy in proxys:
					pidfile.write(proxy + '\n')
			else:
				pidfile.write(proxys + '\n')
			pidfile.close()
			break
		except:
			# print "another instance is running..."
			time.sleep(3)

def upgradeWiseproxy(proxys):
	'''登陆 删除原有wiseproxy 更新新的wiseproxy'''
	dir_r =  os.path.dirname(os.path.abspath(__file__))
	etc_c = os.path.join(dir_r, 'wiseproxy.conf')
	print etc_c
	cf = ConfigParser.ConfigParser()
	cf.read(etc_c)
	login_url = cf.get('main', 'login_url')
	api_url = cf.get('main', 'api_url')
	usr_pwd_data = eval(cf.get('main', 'usr_pwd_data'))
	headers = {'Content-type': 'application/x-www-form-urlencoded', 'charset': 'utf-8'}
	# login
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	req = urllib2.Request(login_url, urlencode(usr_pwd_data), headers)
	opener.open(req)
	#delete old proxy
	queryurl='http://wiseproxy.ops.vobile.org/getProxyList?partitionSearch=buy&proxySearch=&_search=false&nd=1503380267574&rows=500&page=1&sidx=&sord=asc'
	#http://wiseproxy.ops.vobile.org/getProxyList?partitionSearch=&proxySearch=120.55.115.209:63267&_search=false&nd=1503563948157&rows=10&page=1&sidx=&sord=asc
	oldproxys = opener.open(queryurl).read()
	oldproxys=json.loads(oldproxys)
	oldproxylist=oldproxys['rows']
	for oldproxy in oldproxylist:
		proxyid =  oldproxy['id']
		print proxyid

	sys.exit()
	if type(proxys)==type([]):
		# addproxy
		for proxy in proxys:
			data = {"partition": "9509", "proxyId": -1, "proxyServerInfo": proxy, "source": "Vultr"}
			request = urllib2.Request(api_url, urlencode(data), headers)
			response = opener.open(request)
	else:
		data = {"partition": "9509", "proxyId": -1, "proxyServerInfo": proxys, "source": "Vultr"}
		request = urllib2.Request(api_url, urlencode(data), headers)
		response = opener.open(request)
	opener.close()

#upgradeWiseproxy('192.168.200.252:3127')
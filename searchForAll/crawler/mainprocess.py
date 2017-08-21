#coding=utf8
import importlib
import urllib

#后面：去重功能 结果穿插排序功能

def keywordSearch(keyword):
	print keyword
	keyword = urllib.quote(keyword.encode('utf8'))
	SITES = {
		'baidu': 'https://www.baidu.com/s?wd='+keyword,
		'bing':'https://www.bing.com/search?q=%s&pc=MOZI&form=MOZSBR'%keyword

	}  # 域名和模块对应关系
	import sys
	#print sys.path
	response=[]
	for k,v in SITES.items():
		mo = importlib.import_module('.'.join(['searchForAll','crawler','extractors', k]))
		response+=(mo.process(v))
		#print v

	return response
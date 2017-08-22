#coding=utf8
import importlib
import urllib
import threading
import Queue
#后面：去重功能 结果穿插排序功能 生成翻页地址 默认的页面自动解析 同步访问 代理访问（统一就是一个访问接口/函数，接受一堆链接去同步调各种代理访问，响应结果） 同一网站多入口

def keywordSearch(keyword,page='1',type='0'):
	TYPES={'0':'searchEngine','1':'movie','2':'music','3':'novel','4':'news','5':'code'}
	print keyword
	keyword = urllib.quote(keyword.encode('utf8'))
	type=str(type)
	page=int(page)
	if type == '0':
		SITES = {
			'baidu': 'https://www.baidu.com/s?wd=%s&pn=%s&ie=utf-8'%(keyword,str(page*10)),
			'bing':'https://www.bing.com/search?q=%s&pc=MOZI&form=MOZSBR&first=%s&FORM=PERE%s'%(keyword,str(page*10+1),page)

		}  # 域名和模块对应关系
	elif type == '5':
		SITES = {
			'githubReposity': 'https://github.com/search?q=%s&p=%s&type=Repositories' % (keyword, str(page)),
		}  # 域名和模块对应关系

	else:
		SITES = {
			'baidu': 'https://www.baidu.com/s?wd=%s&ie=utf-8' % (keyword)
		}

	response=[]

	class MyThread(threading.Thread):

		def __init__(self, func, args=()):
			super(MyThread, self).__init__()
			self.func = func
			self.args = args

		def run(self):
			self.result = self.func(*self.args)

		def get_result(self):
			try:
				return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
			except Exception:
				return None

	li = []
	for k,v in SITES.items():
		mo = importlib.import_module('.'.join(['searchForAll','crawler','extractors', k]))#这个地方需要并发
#		response+=(mo.process(v))
		t = MyThread(mo.process,args=[v])
		print v
		li.append(t)
		t.start()


	for t in li:
		t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
		print t.get_result()
		response += t.get_result()


	#print v
	#根据url去重
	sortedResponse={}
	for result in response:
		sortedResponse[result.get('url')]=result
	response=[]
	for k,v in sortedResponse.items():
		response.append(v)


	return response
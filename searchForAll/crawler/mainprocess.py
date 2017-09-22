#coding=utf8
import importlib
import urllib
import threading
import Queue
#后面：去重功能 结果穿插排序功能 生成翻页地址 默认的页面自动解析 同步访问 代理访问（统一就是一个访问接口/函数，接受一堆链接去同步调各种代理访问，响应结果） 同一网站多入口
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from calculate import similarCal

def keywordSearch(keyword,page='1',type='0'):
	TYPES={'0':'searchEngine','1':'movie','2':'music','3':'novel','4':'news','5':'code'}
	keywordbf=keyword
	keyword = urllib.quote(keyword.encode('utf8'))  #输入的是str
	print keyword
	type=str(type)
	page=int(page)
	websitelist={
		1:{'baidu':'https://www.baidu.com/s?wd=%s&pn=%s&ie=utf-8'%(keyword,page*10)},
		2:{'bing':'https://www.bing.com/search?q=%s&pc=MOZI&form=MOZSBR&first=%s&FORM=PERE%s'%(keyword,page*10+1,page)},
		3:{'taobao':'https://s.taobao.com/search?q=%s&s=%s' % (keyword, (page-1)*44)},
		4:{'jd':'https://search.jd.com/Search?keyword=%s&page=%s&enc=utf-8'%(keyword,page*2+1)},
		5:{'amazon':'https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&rh=i%3Aaps%2Ck%3A'+keyword+'&page='+str(page)},
		6:{'google':'https://www.google.com/search?q=%s&start=%s&num=100'%(keyword,page*100)},
		7:{'githubReposity': 'https://github.com/search?q=%s&p=%s&type=Repositories' % (keyword, page)},#github
		8:{'tmall':'https://list.tmall.com/search_product.htm?q=%s&s=%s'%(keyword,page*60)},#天猫
		9:{'suning':'https://search.suning.com/%s/&iy=0&cp=%s'%(keyword,page-1)}, #苏宁
		10:{'dangdang':'http://search.dangdang.com/?key=%s&act=input&page_index=%s'%(keyword,page)},
		11:{'gome':'https://search.gome.com.cn/search?question=%s&searchType=goods&facets=12gm&page=%s&bws=0&type=json&rank=1'%(keyword,page)},

		#资源搜索
		12:{'mj0351':'https://sou.mj0351.com/search.html?text=%s&page=%s&sort=0&searchtype=0'%{keyword,page}},
		13:{'cilimao':'http://www.cilimao.me/api/search?size=10&sortDirections=desc&word=%s&page=%s'%{keyword,page}},
		14:{'moviejie':'https://moviejie.com/search/q_%s/'%(keyword)}, #感觉不太好
		15:{'591mov':'https://591mov.com/zh-hans/search/soe/?c=&s=create_time&p=%s'%{keyword,page}},
		16:{'56wangpan':'http://www.56wangpan.com/search/kw%spg%s'%(keyword,page)},
   		17:{'slimego':'http://www.slimego.cn/search.html?q=game%20of&page=2&rows=20'},




		}

	websiteType={
		"searchEngine":[1,2,6],
		"shopping":[3,4,5,8,9,10],
		"Scholar":[],
		"travel":[],#http://scholar.chongbuluo.com/
		"downloads":[],
		"dataAnalyse":[],#http://data.chongbuluo.com/
		"onlineMovies":[],
		"music":[],
		"novel":[],
		"news":[],
		"blog_it":[]

	}
	if type == '0' or type == 'null':
		SITES = dict(websitelist[1].items()+websitelist[2].items())
 # 域名和模块对应关系
	elif type == '1':
		SITES  = dict(websitelist[3].items()+websitelist[4].items()+websitelist[5].items())
	elif type == '2':
		SITES = dict(websitelist[6].items())

	elif type == '5':
		SITES = dict(websitelist[7].items())

	else:
		SITES = dict(websitelist[1].items())

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
		#print v
		li.append(t)
		t.start()


	for t in li:
		t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
		#print t.get_result()
		rs = t.get_result()
		if rs:
			response += rs


	#print v
	#根据url去重
	sortedResponse={}
	for result in response:
		sortedResponse[result.get('url')]=result
	response=[]
	for k,v in sortedResponse.items():#暂且根据长度排列？
		response.append(v)
	#print response
	#response需要来个智能排序
	rsAfterSort=None
	if type == '1': #目前看来商品的结果比较合适用关键词排序
		try:
			rsAfterSort = similarCal.sortBySimilar(response,'title',firstkeyword=keywordbf)
		except Exception, e:
			print str(e)
	if rsAfterSort:
		response=rsAfterSort


	return response
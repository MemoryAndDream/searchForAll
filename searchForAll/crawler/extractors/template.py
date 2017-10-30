#coding=utf8
from ..common import crawlerTool as ct
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def process(url):
	urlinsfos=[]
	page = ct.crawlerTool.getPage(url)
	#print page
	#print url
	segments = ct.crawlerTool.getXpath('//div[@class="result c-container "]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		try:
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//a[1]/@href',segment)[0]#好像是/text()会起到转码功能
			urlinfo['title'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//a[1]//text()',segment))
			urlinfo['info'] =  ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class ="c-abstract"]//text()', segment))
			#print urlinfo['url'],urlinfo['title'],urlinfo['info']
			urlinsfos.append(urlinfo)
		except:
			print('error')
			traceback.print_exc()
	return {"urlinsfos":urlinsfos}


#需要去testSiteConfig.py里测试

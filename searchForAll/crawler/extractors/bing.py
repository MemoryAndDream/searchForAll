#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys




#相对导入不能超过最高层
def process(url):
	urlinsfos=[]
	page = ct.crawlerTool.getPage(url)
	#print page
	segments = ct.crawlerTool.getXpath('//li[@class="b_algo"]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		urlinfo={}
		urlinfo['url']= ct.crawlerTool.getXpath('//h2/a[1]/@href',segment)[0]
		title = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h2/a[1]', segment)[0])).encode('unicode-escape').decode('string_escape')
		#print title,HTMLParser().unescape(title)
		#print ct.crawlerTool.getXpath('//h2/a[1]', segment)
		urlinfo['title'] = title
		urlinfo['info'] = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class="b_caption"]', segment)[0])).encode('unicode-escape').decode('string_escape')
		urlinsfos.append(urlinfo)
	return urlinsfos



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")
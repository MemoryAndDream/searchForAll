#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback



def process(keyword,page):
	url='https://search.jd.com/Search?keyword=%s&page=%s&enc=utf-8'%(keyword,page*2+1)
	urlinfos=[]
	page = ct.crawlerTool.getPage(url)
	segments = ct.crawlerTool.getXpath("//li[@class='gl-item']",page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		try:
			#print segment
			urlinfo={}
			urlinfo['url']= ct.getXpath('//a/@href',segment)[0]
			urlinfo['title'] =  HTMLParser().unescape(ct.getRegex('a target="_blank" title="(.*?)"',segment))
			if urlinfo['title']:	urlinfo['title'] =urlinfo['title'] +u'-京东'#书籍的结果页面不一样
			else:
				#print segment
				urlinfo['title'] =HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[contains(@class,"p-name")]//a[@target="_blank"]', segment)[0])) +u'-京东'

			data_price =  ct.getRegex('data-price="(.*?)"',segment)

			if not data_price:
				data_price=HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[contains(@class,"p-price")]//strong', segment)[0]))
				urlinfo['info'] =  '价格<em>%s</em>元'%(data_price)
			else:urlinfo['info'] = '价格<em>%s</em>元'%(data_price)

			imglink = ct.getXpath('//img/@src',segment)
			if imglink:
				imglink=imglink[0]
			else:
				imglink=ct.getXpath('//img/@data-lazy-img',segment)
				if imglink:
					imglink = imglink[0]
				else:imglink=None


			urlinfo['imglink'] =  imglink

			#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
			if urlinfo['title']:
				urlinfos.append(urlinfo)
		except:#有些奇怪的格式是会解析失败的
			pass
	return {"urlinfos":urlinfos}



def test():
	return process("https://s.taobao.com/search?q=python")
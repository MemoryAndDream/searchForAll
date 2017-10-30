#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback



def process(keyword,page):#国美的价格是用的ajax请求生成的，卧槽
	url='https://search.gome.com.cn/search?question=%s&searchType=goods&&page=%s'%(keyword,page)
	urlinfos=[]
	page = ct.crawlerTool.getPage(url)
	segments = ct.crawlerTool.getXpath('//div[contains(@class,"item-tab")]',page)#这个xpath可以过滤掉很多广告。。
	print len(segments)
	if len(segments)==0:print page
	for segment in segments:
		try:
			#print segment
			urlinfo={}
			urlinfo['url']= ct.getXpath('//a[contains(@class,"item-link")]/@href',segment)[0]
			urlinfo['title'] =  HTMLParser().unescape(ct.getXpath('//a/@title',segment)[0])
			if urlinfo['title']:	urlinfo['title'] =urlinfo['title'] +u'-国美'#书籍的结果页面不一样

			data_price =  ct.getXpath('//span[contains(@class,"price asynPrice")]',segment)
			if data_price:
				urlinfo['info'] =  '价格<em>%s</em>元'%(data_price[0])

			imglink = ct.getXpath('//a[@class="item-link"]/img/@src',segment)
			if imglink:
				imglink=imglink[0]

			else:
				imglink = ct.getXpath('//img/@gome-src', segment)
				if imglink:
					imglink = imglink[0]
					#print imglink


			urlinfo['imglink'] =  imglink

			#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
			if urlinfo['title']:
				urlinfos.append(urlinfo)
		except:#有些奇怪的格式是会解析失败的
			traceback.print_exc()
	return {"urlinfos":urlinfos}



def test():
	return process("https://s.taobao.com/search?q=python")
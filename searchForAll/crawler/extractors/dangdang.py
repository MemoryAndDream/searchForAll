#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback



def process(keyword,page):
	url='http://search.dangdang.com/?key=%s&act=input&page_index=%s'%(keyword,page)
	urlinfos=[]
	page = ct.crawlerTool.getPage(url,pageCharset='gb2312')
	segments = ct.crawlerTool.getXpath('//li[contains(@class,"line")]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		try:
			#print segment
			urlinfo={}
			urlinfo['url']= ct.getXpath('//a/@href',segment)[0]
			urlinfo['title'] =  HTMLParser().unescape(ct.getXpath('//a/@title',segment)[0])
			if urlinfo['title']:	urlinfo['title'] =urlinfo['title'] +u'-当当'#书籍的结果页面不一样

			data_price =  ct.getXpath('//span[contains(@class,"price")]',segment)[0]
			urlinfo['info'] =  '价格<em>%s</em>元'%(data_price)

			imglink = ct.getXpath('//a[@class="pic"]/img/@data-original',segment)
			if imglink:
				imglink=imglink[0]
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
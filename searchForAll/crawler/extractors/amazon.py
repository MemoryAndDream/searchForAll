#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback



def process(keyword,page):
	url='https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&rh=i%3Aaps%2Ck%3A'+keyword+'&page='+str(page)
	urlinfos=[]
	page = ct.crawlerTool.getPage(url)
	segments = ct.crawlerTool.getXpath("//li[contains(@id,'result')]",page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		try:
			#print segment
			urlinfo={}
			urlinfo['url']= ct.getXpath('//a[contains(@class,"a-link-normal")]/@href',segment)[0]
			urlinfo['title'] =HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h2', segment)[0])) +u'-亚马逊'

			data_price = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//span[contains(@class,"s-price")]', segment)[0]))
			urlinfo['info'] = '价格<em>%s</em>元'%(data_price)
			imglink = ct.getXpath('//img[contains(@class,"s-access-image")]/@src',segment)[0]



			urlinfo['imglink'] =  imglink

			#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
			if urlinfo['title']:
				urlinfos.append(urlinfo)
		except:#有些奇怪的格式是会解析失败的
			pass
	return {"urlinfos":urlinfos}



def test():
	return process("https://s.taobao.com/search?q=python")
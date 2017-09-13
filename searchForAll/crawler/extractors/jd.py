#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback
# 摘取所要数据
def parsePage( html):
	ilt=[]
	try:
		plt = re.findall(r'data-price=".*?"', html)
		tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
		npl = re.findall(r'\"view_sales\"\:\"[\d]*', html)
		nid = re.findall(r'\"nid\"\:\"[\d]*', html)
		imglinks=re.findall(r'"pic_url":".*?"', html)
		for i in range(len(plt)):
			price = eval(plt[i].split('=', 1)[1])
			title = eval(tlt[i].split(':', 1)[1])
			num = eval(npl[i].split(':"', 1)[1])
			url = 'https://detail.tmall.com/item.htm?id='+str(eval(nid[i].split(':"', 1)[1]))
			imglink=imglinks[i].split(':', 1)[1].replace('"','')

			ilt.append({'price':price, 'num':num, 'title':title,'url':url,'imglink':imglink})
		return ilt
	except:
		traceback.print_exc()
		print("摘取数据出错").encode('utf-8')
		return None


def process(url):
	urlinsfos=[]
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
			imglink = ct.getXpath('//img/@src',segment)
			if imglink:
				imglink=imglink[0]
			else:
				imglink=ct.getXpath('//img/@data-lazy-img',segment)
				if imglink:
					imglink = imglink[0]
				else:imglink=None
			urlinfo['info'] = '价格%s元'%(data_price)
			urlinfo['imglink'] =  imglink

			#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
			if urlinfo['title']:
				urlinsfos.append(urlinfo)
		except:#有些奇怪的格式是会解析失败的
			pass
	return urlinsfos



def test():
	return process("https://s.taobao.com/search?q=python")
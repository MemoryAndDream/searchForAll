#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

# 摘取所要数据
def parsePage( html):
	ilt=[]
	try:
		plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
		tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
		npl = re.findall(r'\"view_sales\"\:\"[\d]*', html)
		nid = re.findall(r'\"nid\"\:\"[\d]*', html)
		for i in range(len(plt)):
			price = eval(plt[i].split(':', 1)[1])
			title = eval(tlt[i].split(':', 1)[1])
			num = eval(npl[i].split(':"', 1)[1])
			url = 'https://detail.tmall.com/item.htm?id='+nid
			ilt.append({'price':price, 'num':num, 'title':title,'url':url})
		return ilt
	except:
		print("摘取数据出错").encode('utf-8')
		return None


def process(url):
	urlinsfos=[]
	page = ct.crawlerTool.getPage(url)
	segments = ct.crawlerTool.getXpath('//li[@class="b_algo"]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		segment=segment.replace('&#183;','')
		urlinfo={}
		urlinfo['url']= ct.crawlerTool.getXpath('//h2/a[1]/@href',segment)[0]

		title = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h2/a[1]', segment)[0]))#好像不转str格式后面输出是乱码S

		urlinfo['title'] = title
		urlinfo['info'] = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class="b_caption"]', segment)[0]))
		print urlinfo['url'], urlinfo['title'], urlinfo['info']
		urlinsfos.append(urlinfo)
	return urlinsfos



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")
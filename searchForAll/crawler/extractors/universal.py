#coding=utf8
'''
通过配置的网站
目前使用于情况不多的网站
传入 keyword page website


'''

from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import ConfigParser

def process(keyword,page,website):  #后面需要分类型

	siteconfs=os.listdir(os.path.dirname(os.path.abspath(__file__))+'/siteconfs')
	if not website in siteconfs:
		print 'siteconf not found'
		return []
	confpath = os.path.dirname(os.path.abspath(__file__))+'/siteconfs/'+website
	siteconf = ConfigParser.ConfigParser()
	siteconf.read(confpath)
	extractors = siteconf.sections()
	try:
		extractors = sorted(extractors,key=lambda d: int(d[-1]))
	except:pass
	for extractor in extractors:
		url = siteconf.get(extractor,'searchUrl')
		url = url.replace('${keyword}',keyword).replace('${page}',str(page))
		segmentCut = siteconf.get(extractor,'segment')
		titleCut =  siteconf.get(extractor,'title')
		urlCut = siteconf.get(extractor, 'url')
		infoCuts =  siteconf.get(extractor, 'info')
		urlinsfos=[]#bing页面结果与百度不同 百度输出已经是\uxxx格式了 bing还是\xe1格式(str) 所以需要先解码成unicode
		pageBuf = ct.crawlerTool.getPage(url)#print HTMLParser().unescape('&#183;').encode('unicode-escape').decode('string_escape')是乱码
		segments = ct.crawlerTool.getXpath(segmentCut,pageBuf)#这个xpath可以过滤掉很多广告。。
		if not segments:continue
		for segment in segments:
			try:
				urlinfo={}
				urlinfo['url']= ct.crawlerTool.getXpath(urlCut,segment)[0]

				title = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath(titleCut, segment)[0]))#好像不转str格式后面输出是乱码S
				#print title,HTMLParser().unescape(title)
				#print ct.crawlerTool.getXpath('//h2/a[1]', segment)#解码后&#183;好像变乱码了
				urlinfo['title'] = title
				print title
				urlinfo['info']=''
				for infoCut in infoCuts.split(';'):
					urlinfo['info'] += ct.crawlerTool.getXpath(infoCut, segment)[0]
				#print urlinfo['url'], urlinfo['title'], urlinfo['info']
				urlinsfos.append(urlinfo)
			except Exception,e:
				traceback.print_exc()

		return urlinsfos



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")


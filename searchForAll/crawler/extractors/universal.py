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
from ..common import urlHostParser


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
	urlBac=''
	for extractor in extractors:
		url = siteconf.get(extractor,'searchUrl')
		url = url.replace('${keyword}',keyword).replace('${page}',str(page))
		print url
		segmentCut = siteconf.get(extractor,'segment')
		titleCut =  siteconf.get(extractor,'title')
		urlCut = siteconf.get(extractor, 'url')
		infoCuts =  siteconf.get(extractor, 'info')
		urlinfos=[]
		if urlBac == url:#如果是一样的链接就不重复打开了
			pageBuf = ct.crawlerTool.getPage(url)#print HTMLParser().unescape('&#183;').encode('unicode-escape').decode('string_escape')是乱码
		else:
			urlBac = url
			pageBuf = ct.crawlerTool.getPage(url)
		baseurl =  '/'.join(url.split('/')[:3])
		pageBuf = urlHostParser.make_links_absolute(pageBuf,baseurl)
		segments = ct.crawlerTool.getXpath(segmentCut,pageBuf)
		if not segments:
			print 'no matched segments',website
			continue
		for segment in segments:
			try:
				urlinfo={}
				urlinfo['url']= ct.crawlerTool.getXpath(urlCut,segment)[0]

				title = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath(titleCut, segment)[0]))#好像不转str格式后面输出是乱码S
				#print title,HTMLParser().unescape(title)
				#print ct.crawlerTool.getXpath('//h2/a[1]', segment)#解码后&#183;好像变乱码了
				urlinfo['title'] = title
				#print title
				urlinfo['info']=''
				for infoCut in infoCuts.split(';'):
					urlinfo['info'] += ' '.join(ct.crawlerTool.getXpath(infoCut, segment))  #info 作拼接处理
				#print urlinfo['url'], urlinfo['title'], urlinfo['info']
				urlinfos.append(urlinfo)
			except Exception,e:
				traceback.print_exc()

		return {"urlinfos":urlinfos}



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")


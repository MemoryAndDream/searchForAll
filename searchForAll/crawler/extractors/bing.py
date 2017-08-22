#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#bing 没编码，xpath text()结果是\xe5\xe2\x80\x98\xb5\xe5\xe2\x80\x98\xb5  是要从字节码编成str xpath结果是unicode，需要先encode('unicode-escape')再处理
#百度是unicode编码 u'\u5206\u9694', u'\u7b26\u201c\xb7\u201d\u662f\u600e
#要么是xpath有问题

#相对导入不能超过最高层
def process(url):
	urlinsfos=[]
	page = ct.crawlerTool.getPage(url)#print HTMLParser().unescape('&#183;').encode('unicode-escape').decode('string_escape')是乱码
	print url
	segments = ct.crawlerTool.getXpath('//li[@class="b_algo"]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		segment=segment.replace('&#183;','')
		#print segment
		urlinfo={}
		urlinfo['url']= ct.crawlerTool.getXpath('//h2/a[1]/@href',segment)[0]
# u'\xe9\x95\xbf\xe5\x9f\x8e' 需要转码
		title = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h2/a[1]//text()', segment)).encode('unicode-escape').decode('string_escape')
		#print ct.crawlerTool.getXpath('//h2/a[1]', segment)#解码后&#183;好像变乱码了
		urlinfo['title'] = title
		urlinfo['info'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class="b_caption"]//text()', segment)).encode('unicode-escape').decode('string_escape')
		print urlinfo['url'], urlinfo['title'], urlinfo['info']
		urlinsfos.append(urlinfo)
	return urlinsfos



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")
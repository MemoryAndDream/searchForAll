#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

#bing 没编码，xpath text()结果是\xe5\xe2\x80\x98\xb5\xe5\xe2\x80\x98\xb5  是要从字节码编成str xpath结果是unicode，需要先encode('unicode-escape')再处理
#百度是unicode编码 u'\u5206\u9694', u'\u7b26\u201c\xb7\u201d\u662f\u600e
#//text()处理也有问题 唉，目前看来xpath还是只能配合HTMLParser().unescape 使用  不然来回转换坑爹

#相对导入不能超过最高层
def process(keyword,page):
	url='https://www.bing.com/search?q=%s&pc=MOZI&form=MOZSBR&first=%s&FORM=PERE%s'%(keyword,page*10+1,page)
	urlinfos=[]#bing页面结果与百度不同 百度输出已经是\uxxx格式了 bing还是\xe1格式(str) 所以需要先解码成unicode
	page = ct.crawlerTool.getPage(url)#print HTMLParser().unescape('&#183;').encode('unicode-escape').decode('string_escape')是乱码
	#print page
	segments = ct.crawlerTool.getXpath('//li[@class="b_algo"]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		try:
			#print segment
			segment=segment.replace('&#183;','')
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//h2/a[1]/@href',segment)[0]

			title = HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h2/a[1]', segment)[0]))#好像不转str格式后面输出是乱码S
			#print title,HTMLParser().unescape(title)
			#print ct.crawlerTool.getXpath('//h2/a[1]', segment)#解码后&#183;好像变乱码了
			urlinfo['title'] = title
			urlinfo['info'] = ct.crawlerTool.getXpath('//div[@class="b_caption"]', segment)[0]
			#print urlinfo['url'], urlinfo['title'], urlinfo['info']
			urlinfos.append(urlinfo)
		except:
			traceback.print_exc()

	return {"urlinfos":urlinfos}



def test():
	return process("https://www.bing.com/search?q=python&pc=MOZI&form=MOZSBR")
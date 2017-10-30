#coding=utf8
from ..common import crawlerTool as ct
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from HTMLParser import HTMLParser
#相对导入不能超过最高层
def process(keyword,page):
	url='https://www.google.com/search?q=%s&start=%s&num=100'%(keyword,page*100)
	urlinfos=[]
	#urlinfo1={"url":"http://www.baidu.com/link?url=966OdUyxuwFJoAYx_XGYq7_FiVLcej4qEA3Q84e-lLAtLPRGGHA6tsNFNsTN9zka&wd=&eqid=a64931cc000026c3000000035994fd9e","title":"python Django教程 之模板渲染、循环、条件判断、常用的..._博客园","info":'在 W3School,您将找到许多可以在线编辑并测试的 jQuery 实例。 jQuery 实例jQuery 参考手册 在W3School,您将找到包含所有 jQuery 对象和函数的完整参考手册。 jQuery...'}
	page = ct.crawlerTool.getPage(url)
	#print page
	#print url
	segments = ct.crawlerTool.getXpath('//div[@class="g"]',page)
	#print segments
	for segment in segments:
		#print segment
		try:
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//h3/a/@href',segment)[0]#/text()会起到转码功能
			urlinfo['title'] = ct.crawlerTool.getXpath('//h3/a/text()',segment)[0]
			urlinfo['info'] =  HTMLParser().unescape(ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class="s"]', segment)))
			#print urlinfo['url'],urlinfo['title'],urlinfo['info']
			#info里有分隔符的时候出错
			urlinfos.append(urlinfo)
		except:
			print('error')
			traceback.print_exc()
	return {"urlinfos":urlinfos}



def test():
	return process("https://www.baidu.com/s?wd=%E5%88%86%E9%9A%94%E5%8F%B7")
#coding=utf8
from ..common import crawlerTool as ct
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#相对导入不能超过最高层
def process(keyword,page):
	url='https://www.baidu.com/s?wd=%s&pn=%s&ie=utf-8'%(keyword,page*10)
	urlinfos=[]
	#urlinfo1={"url":"http://www.baidu.com/link?url=966OdUyxuwFJoAYx_XGYq7_FiVLcej4qEA3Q84e-lLAtLPRGGHA6tsNFNsTN9zka&wd=&eqid=a64931cc000026c3000000035994fd9e","title":"python Django教程 之模板渲染、循环、条件判断、常用的..._博客园","info":'在 W3School,您将找到许多可以在线编辑并测试的 jQuery 实例。 jQuery 实例jQuery 参考手册 在W3School,您将找到包含所有 jQuery 对象和函数的完整参考手册。 jQuery...'}
	page = ct.crawlerTool.getPage(url)
	#print page
	#print url
	segments = ct.crawlerTool.getXpath('//div[@class="result c-container "]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		try:
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//a[1]/@href',segment)[0]#好像是/text()会起到转码功能
			urlinfo['title'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//a[1]//text()',segment))
			urlinfo['info'] =  ct.crawlerTool.getXpath('//div[contains(@class,"c-abstract")]', segment)[0]
			#print urlinfo['info']
			urlinfo['info-date'] =  ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//span[@class="newTimeFactor_before_abs m"]//text()', segment))
			urlinfo['info-txt'] =  ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class ="c-abstract"]//text()', segment))
			urlinfo['info-url'] =  ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//div[@class ="c-abstract"]//text()', segment))

			#print urlinfo['url'],urlinfo['title'],urlinfo['info']
			#info里有分隔符的时候出错
			urlinfos.append(urlinfo)
		except:
			#print('error')
			traceback.print_exc()

	suggestInfos=[]
	suggestSegments= ct.crawlerTool.getXpath('//div[@id="rs"]//th',page)
	for suggestSegment in suggestSegments:
		#print segment
		try:
			suggestInfo={}
			suggestInfo['url']= ct.crawlerTool.getXpath('//a[1]/@href',suggestSegment)[0]#好像是/text()会起到转码功能
			suggestInfo['title'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//a[1]//text()',suggestSegment))
			suggestInfos.append(suggestInfo)
		except:
			traceback.print_exc()



	return {"urlinfos":urlinfos,"suggestInfos":suggestInfos}



def test():
	return process("https://www.baidu.com/s?wd=%E5%88%86%E9%9A%94%E5%8F%B7")
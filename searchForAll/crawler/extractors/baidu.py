#coding=utf8
from ..common import crawlerTool as ct
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#相对导入不能超过最高层
def process(url):
	urlinsfos=[]
	#urlinfo1={"url":"http://www.baidu.com/link?url=966OdUyxuwFJoAYx_XGYq7_FiVLcej4qEA3Q84e-lLAtLPRGGHA6tsNFNsTN9zka&wd=&eqid=a64931cc000026c3000000035994fd9e","title":"python Django教程 之模板渲染、循环、条件判断、常用的..._博客园","info":'在 W3School,您将找到许多可以在线编辑并测试的 jQuery 实例。 jQuery 实例jQuery 参考手册 在W3School,您将找到包含所有 jQuery 对象和函数的完整参考手册。 jQuery...'}
	page = ct.crawlerTool.getPage(url).replace('·','')
	print page
	print url
	segments = ct.crawlerTool.getXpath('//div[@class="result c-container "]',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		try:
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//a[1]/@href',segment)[0]
			urlinfo['title'] = ct.crawlerTool.getXpath('//a[1]/text()', segment.replace('<em>','').replace('</em>',''))[0]
			urlinfo['info'] = ct.crawlerTool.getXpath('//div[@class ="c-abstract"]/text()', segment.replace('<em>','').replace('</em>',''))[0]
			print urlinfo['url'],urlinfo['title'],urlinfo['info']
			#info里有分隔符的时候出错
			urlinsfos.append(urlinfo)
		except:
			print('error')
			traceback.print_exc()
	return urlinsfos



def test():
	return process("https://www.baidu.com/s?wd=%E5%88%86%E9%9A%94%E5%8F%B7")
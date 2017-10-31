#coding=utf8
from ..common import crawlerTool as ct
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ..common import urlHostParser
#相对导入不能超过最高层
def process(keyword, page):
	url='https://github.com/search?q=%s&p=%s&type=Repositories' % (keyword, page)
	urlinfos=[]
	#urlinfo1={"url":"http://www.baidu.com/link?url=966OdUyxuwFJoAYx_XGYq7_FiVLcej4qEA3Q84e-lLAtLPRGGHA6tsNFNsTN9zka&wd=&eqid=a64931cc000026c3000000035994fd9e","title":"python Django教程 之模板渲染、循环、条件判断、常用的..._博客园","info":'在 W3School,您将找到许多可以在线编辑并测试的 jQuery 实例。 jQuery 实例jQuery 参考手册 在W3School,您将找到包含所有 jQuery 对象和函数的完整参考手册。 jQuery...'}
	page = ct.crawlerTool.getPage(url)
	baseUrl = 'https://github.com'
	page = urlHostParser.make_links_absolute(page,baseUrl)

	#print page
	#print url
	segments = ct.crawlerTool.getXpath('//ul[@class="repo-list"]/div',page)#这个xpath可以过滤掉很多广告。。
	#print segments
	for segment in segments:
		#print segment
		try:
			urlinfo={}
			urlinfo['url']= ct.crawlerTool.getXpath('//h3/a/@href',segment)[0]
			urlinfo['title'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//h3//text()', segment))
			urlinfo['info'] = ct.crawlerTool.extractorText(ct.crawlerTool.getXpath('//p//text()', segment))

			#print urlinfo['url'],urlinfo['title'],urlinfo['info']
			#info里有分隔符的时候出错
			urlinfos.append(urlinfo)
		except:
			print('error')
			traceback.print_exc()
	return {"urlinfos":urlinfos}

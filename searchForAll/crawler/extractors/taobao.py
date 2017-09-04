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
		plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
		tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
		npl = re.findall(r'\"view_sales\"\:\"[\d]*', html)
		nid = re.findall(r'\"nid\"\:\"[\d]*', html)
		imglinks=re.findall(r'"pic_url":".*?"', html)
		for i in range(len(plt)):
			price = eval(plt[i].split(':', 1)[1])
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
	segments = parsePage(page)
	#print segments
	for segment in segments:
		#print segment
		urlinfo={}
		urlinfo['url']= segment.get('url')
		urlinfo['title'] =  segment.get('title')
		if 'tmall' in urlinfo['url']:
			urlinfo['title']=urlinfo['title']+'-天猫'
			urlinfo['source'] = 'tmall'
		else:
			urlinfo['title'] = urlinfo['title'] + '-淘宝'
			urlinfo['source'] = 'taobao'
		urlinfo['info'] = '价格%s元 购买数量%s'%(segment.get('price'),segment.get('num'))
		urlinfo['imglink'] =  segment.get('imglink')

		#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
		urlinsfos.append(urlinfo)
	return urlinsfos



def test():
	return process("https://s.taobao.com/search?q=python")
#coding=utf8
from ..common import crawlerTool as ct
from HTMLParser import HTMLParser#这个出来是unicode的格式，后面没法弄
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import traceback
import json
# 摘取所要数据


def process(keyword,page):
	url='https://s.taobao.com/search?q=%s&s=%s' % (keyword, (page-1)*44)
	urlinfos=[]
	page = ct.crawlerTool.getPage(url)

	g_page_config =ct.crawlerTool.getRegex('g_page_config\s*=\s*(.*);',page)
	#print eval(g_page_config)['mod']['data']['auctions']
	try:
		segments = json.loads(g_page_config)['mods']['itemlist']['data']['auctions']  #搜索微波炉就不用这个了
	except:
		segments = []
	if segments:
		#print segments[0]
		for segment in segments:
			try:
				#print segment
				urlinfo={}
				urlinfo['url']='https://detail.tmall.com/item.htm?id='+segment['nid']
				urlinfo['title'] = segment['raw_title']
				if 'tmall' in urlinfo['url']:
					urlinfo['title']=urlinfo['title']+'-天猫'
					urlinfo['source'] = 'tmall'
				else:
					urlinfo['title'] = urlinfo['title'] + '-淘宝'
					urlinfo['source'] = 'taobao'
				num=segment.get('view_sales','0')
				price = segment["view_price"]
				urlinfo['info'] = '价格<em>%s</em>元 购买数量<em>%s</em>'%(price,num)
				urlinfo['imglink'] = segment["pic_url"]

				#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
				urlinfos.append(urlinfo)
			except:
				traceback.print_exc()


	else:
		segments = json.loads(g_page_config)['mods']['grid']['data']['spus']
		for segment in segments:
			try:
				#print segment
				urlinfo={}
				urlinfo['url']=segment['url']
				urlinfo['title'] = segment['title']
				if 'tmall' in urlinfo['url']:
					urlinfo['title']=urlinfo['title']+'-天猫'
					urlinfo['source'] = 'tmall'
				else:
					urlinfo['title'] = urlinfo['title'] + '-淘宝'
					urlinfo['source'] = 'taobao'
				importantKey = segment['importantKey']
				price = segment["price"]
				urlinfo['info'] = '价格<em>%s</em>元 <em>%s</em> '%(price,importantKey)
				urlinfo['imglink'] = segment["pic_url"]

				#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
				urlinfos.append(urlinfo)
			except:
				traceback.print_exc()



	return {"urlinfos":urlinfos}



def test():
	return process("https://s.taobao.com/search?q=python")
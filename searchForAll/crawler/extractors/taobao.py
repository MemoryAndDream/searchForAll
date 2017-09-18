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


def process(url):
	urlinsfos=[]
	page = ct.crawlerTool.getPage(url)

	g_page_config =ct.crawlerTool.getRegex('g_page_config\s*=\s*(.*);',page)
	#print eval(g_page_config)['mod']['data']['auctions']
	segments = json.loads(g_page_config)['mods']['itemlist']['data']['auctions']
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
			urlinfo['info'] = '价格%s元 购买数量%s'%(price,num)
			urlinfo['imglink'] = segment["pic_url"]

			#print urlinfo['url'], urlinfo['title'], urlinfo['info'],urlinfo['imglink']
			urlinsfos.append(urlinfo)
		except:
			traceback.print_exc()
	return urlinsfos



def test():
	return process("https://s.taobao.com/search?q=python")
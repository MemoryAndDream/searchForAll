#! /usr/bin/python
#coding=utf-8
'''
@author Meng_Zhihao
@mail 312141830@qq.com
'''
import sys
import urllib
import urllib2
import re
import os
import cookielib
import json
from lxml import etree
import Queue
reload(sys)
sys.setdefaultencoding('utf-8')
import threading
import commands

#下一步升级：将proxy，cookie做入类变量处理 用字典处理cookie覆盖
#用字典构造



class requestPars:
    PROXY = 'proxy'
    USER_AGENT = 'userAgent'
    DATA = 'data'
    COOKIE = 'cookie'


#通用方法
class crawlerTool:
    #类的全局变量
    def __init__(self):
        pass

    #基本的页面访问 输出页面
    #getPage(url,data=xx)  getPage(url,requestPars.=xx)
    @staticmethod
    def getPage(url,proxy=None,data=None, referer = None ,cookie = None ,userAgent = None,cookiePath=None,pageCharset='utf8'):
        # print url
        page_buf = ''
        #参考colander逻辑，链接带"的视作post请求
        if '"' in url:
            r = url.split('"')
            url,data=r[0],r[1]
        i = 0  #重试次数
        for i in range(1):
           # print url
            try:
                if proxy:
                    handlers = [urllib2.ProxyHandler({'http': 'http://%s/' % proxy,'https': 'http://%s/' % proxy})]
                    opener = urllib2.build_opener(*handlers)
                else:
                    opener = urllib2.build_opener()
                method = urllib2.Request(url,data)
                if referer:
                    method.add_header('Referer', referer)
                if cookiePath:
                    method.add_header('Cookie', crawlerTool.readCookie(cookiePath))
                if cookie:
                    method.add_header('Cookie', cookie)
                if userAgent:
                    method.add_header('User-Agent',
                                      userAgent)
                else:
                    method.add_header('User-Agent',
                                  'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:41.0) Gecko/20100101 Firefox/41.0')
                method.add_header('Accept-Language', 'en-US,en;q=0.5')
                result = opener.open(method, timeout=10)

                page_buf = result.read()
                page_buf=page_buf.decode(pageCharset,'ignore')
               # print page_buf

                return page_buf

            except urllib2.URLError, reason:
                if 'sslv3 alert handshake failure' in str(reason):
                    cmd = "curl '" + url + "' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0'"
                    pagebuf = commands.getoutput(cmd)
                    return pagebuf
                return str(reason)
            except Exception, reason:
                raise Exception(reason)
        pass

    #getPageByPostJson data input is a dict
    #getPage(url,data=xx)  getPage(url,requestPars.=xx)
    @staticmethod
    def getPageByJson(url,proxy=None,data={}, referer = None ,cookie = None ,userAgent = None,cookiePath=None):
        page_buf = ''
        i = 0
        for i in range(1):
            # print url
            try:
                if proxy:
                    handlers = [urllib2.ProxyHandler({'http': 'http://%s/' % proxy,'https': 'http://%s/' % proxy})]
                    opener = urllib2.build_opener(*handlers)
                else:
                    opener = urllib2.build_opener()
                if type(data) == type({}):data=json.dumps(data)
                method = urllib2.Request(url,data=data)#要注意None对应null
                method.add_header('Content-Type','application/json')
                if referer:
                    method.add_header('Referer', referer)
                if cookiePath:
                    method.add_header('Cookie', crawlerTool.readCookie(cookiePath))
                if cookie:
                    method.add_header('Cookie', cookie)
                if userAgent:
                    method.add_header('User-Agent', userAgent)
                else:
                    method.add_header('User-Agent',
                                  'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36')
                method.add_header('Accept-Language', 'en-US,en;q=0.5')
                result = opener.open(method, timeout=10)
                page_buf = result.read().encode('utf8')
                return page_buf
            except urllib2.URLError, reason:
                return str(reason)
            except Exception, reason:
                raise Exception(reason)

    #获取正则的第一个匹配
    @staticmethod
    def getRegex(pattern,content):
        group = re.search(pattern, content)
        if group:
            return group.groups()[0]
        else:
            return ''

    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码
        tree = etree.HTML(content)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result))
        return out

    #去掉<>里的内容  这个方法会导致转义字符变回去！！！坑爹
    @staticmethod
    def extractorText(content):
        if type(content)==type([]):
            rs=''
            for record in content:
                rs+=(re.sub('(<[^>]*?>)',"",record))
            return rs
        return re.sub('(<[^>]*?>)',"",content)



    # 获取跳转链接
    @staticmethod
    def getDirectUrl(url):
        u = urllib2.urlopen(url)
        redirectUrl = u.geturl()
        return redirectUrl

    #输出页面的各种信息 输出字典
    @staticmethod
    def getPageDetail(url,proxy=None,data=None, referer = None ,cookie = None ,userAgent = None,cookiePath=None):
        PageDetail = {}
        page_buf = ''
        n = 1
        for i in range(n):
            # print url
            try:
                getCookie = cookielib.CookieJar()
                cookieHandler = urllib2.HTTPCookieProcessor(getCookie)
                if proxy:
                    handlers = [urllib2.ProxyHandler({'http': 'http://%s/' % proxy,'https': 'http://%s/' % proxy}),cookieHandler]
                    opener = urllib2.build_opener(*handlers)
                else:
                    opener = urllib2.build_opener(cookieHandler)
                method = urllib2.Request(url,data)
                if referer:
                    method.add_header('Referer', referer)
                if cookiePath:
                    method.add_header('Cookie', crawlerTool.readCookie(cookiePath))
                if cookie:
                    method.add_header('Cookie', cookie)
                if userAgent:
                    method.add_header('User-Agent',
                                      userAgent)
                else:
                    method.add_header('User-Agent',
                                  'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36')
                method.add_header('Accept-Language', 'en-US,en;q=0.5')
                result = opener.open(method, timeout=10)
                #print str(result.headers)
                page_buf = result.read()

                PageDetail['pageContent']=page_buf
                PageDetail['code'] = 200
                cookie_str = ''
                for item in getCookie:
                    cookie_str += item.name + "=" + item.value + "; "
                PageDetail['cookie'] = cookie_str
                #print 'getcookie:'+cookie_str

                break
            except urllib2.HTTPError, e:
                #print e.reason
                PageDetail['code'] = e.code
                PageDetail['cookie'] =e.headers.get('Set-Cookie','')  #这里是因为百度403错误仍然需要取cookie
                #print e.headers.get('Set-Cookie','')

            except urllib2.URLError, reason:
                #print reason.read()
                PageDetail['code'] = 1003
                #print 'URLError'+str(reason)
                break
            except Exception, reason:
                if i == n:
                    #print 'Error'+str(reason)
                    break

        return PageDetail

    #保存cookie 如果路径不存在就新建  如果不是需要分开写可以用cookielib.MozillaCookieJar(filename)
    @staticmethod
    def saveCookie(cookie,path):
        if os.path.isdir(path):
            sys.exit(0)
        try:
            if not os.path.exists(path):
                parent_path = os.path.dirname(path)
                if not os.path.exists(parent_path):os.makedirs(parent_path)  #建立级联目录
                with open(path,'w') as f:
                    f.write(cookie)
            else:
                with open(path,'w') as f:
                    f.write(cookie)
        except:
            sys.exit(0)



    # 读取cookie
    @staticmethod
    def readCookie(path):
        if not os.path.isfile(path):
            return ''
        else:
            with open(path,'r') as f:
                return f.read()
        pass

    def threadRequest(self,urls):


        '''同步访问多条链接'''
        response={}
        # 初始化队列
        myqueue = Queue.Queue(maxsize=0)  # 设置maxsize<=0则不限制大小
        def getPages():
            while not myqueue.empty():  # 等进程完了也就完了
                url = myqueue.get()
                response['url']=self.getPage(url)
        for url in urls:
            myqueue.put(url)

        threadnum = len(urls)  # 尝试过的50个线程 直接print>>f写法是可以的,用queue输出比较慢。。  或者应该用锁来作输出
        threads = []
        for i in range(threadnum):
            t = threading.Thread(target=getPages)
            t.start()
            threads.append(t)
        for i in range(threadnum):
            threads[i].join(5)  # join看是不是都执行完了
        return response



def keywordSearch(maxPageNum,keyword,proxy=''):
    try:
        #print proxy
        #print keyword,'do list search'
        keyword = keyword.replace(' ','+')
        pageNum = 0
        urlListDepth0 = []
        urlDepth0 = 'https://www.youtube.com/results?search_query='+keyword
        finalResult = []
        for pageNum in range(maxPageNum):

            pageDepth0 = crawlerTool.getPage(urlDepth0,proxy=proxy)
            #print pageDepth0
            urlDepth1 =  re.findall('class="yt-lockup-title\s*"><a href="(/watch\?v=[\w_-]+&amp;list=[^"]+)"',pageDepth0)
            urlDepth0 = 'https://www.youtube.com'+crawlerTool.getRegex('<a href="(.*?)"[^>]+"><span class="yt-uix-button-content">Next',pageDepth0)
            #print urlDepth0
            urlListDepth1 = []
            for url in urlDepth1:
                url = url.replace('&amp;','&')
                url = 'https://www.youtube.com'+url
                if not url in urlListDepth1:
                    #print url
                    urlListDepth1.append(url)
            #print urlListDepth1,len(urlListDepth1)
            urlListDepth2 = []
            for url in urlListDepth1:
                #print 'open listUrl:',url
                pageDepth1 = crawlerTool.getPage(url,proxy=proxy).replace('&amp;','&')
                urlDepth2  =re.findall('(/watch\?v=[^"]*)\&index=\d+',pageDepth1)
                for urlDepth2 in urlDepth2:
                    if not urlDepth2 in urlListDepth2:
                        urlDepth2 = 'http://www.youtube.com'+urlDepth2
                        finalResult.append(urlDepth2)
                        #print urlDepth2
                        urlListDepth2.append(urlDepth2)
        #print len(finalResult),finalResult
        return finalResult
    except:
        print 'do listSearch failed'

#需要输入关键字和最大页数 输出hostingurl列表 这脚本只覆盖playlist链接



instanceList = []

def new_instance():
    newInstance = crawlerTool()
    instanceList.append(newInstance)
    return newInstance

originInstance = new_instance()
getPage = originInstance.getPage
getPageByJson = originInstance.getPageByJson
getRegex = originInstance.getRegex
getXpath = originInstance.getXpath
extractorText = originInstance.extractorText



if __name__ == '__main__':
   # sys.exit()
    ct=crawlerTool()
    data=       {
     "keyid": "abcdefghijk2ml2n83",
     "website": "Kuwo",
     "url": "http://www.filebox.com",
     "author":"bb",
     "author_url": "http://www.filebox.com/?v=293280JUN0102",
     "post_date": "2015-03-20 1:12:50",
      "hide_flag2" : 0,
     "duration":225
   }
    #print ct.threadRequest(['https://www.bing.com/search?q=%E5%91%B5%E5%91%B5','https://www.baidu.com/s?wd=python'])
    page = getPage('https://www.pornhub.su/rss').encode('utf8')
    #print getXpath('//link',page)
    print re.findall('link>(.*?viewkey.*?)<',page)
    #keyword=urllib.quote('呵呵')
    #page= ct.getPage('https://stackoverflow.com/search?q=%E4%B8%AD%E6%96%87')
    #print page
    #with open('1.html','w') as f:
    #    f.write(page)
   # print json.dumps(data)
   # print ct.getPageByJson('http://192.168.1.72:8080/VTServiceFK/service/updateVideoInfo',data=data)
    #print ct.getXpath('//title',page)
    #print ct.getXpath('//title/text()',page)#这个输出很奇怪 bing是 u'\x6e\x5b'这样的，国内是u'\uxxxx' 说明国内外网站默认编码不同，页面上写的utf8是解码方式,不过一个是unicode变utf8，一个是str变utf8
    #sys.exit()
    #print ct.getDirectUrl('http://v.qq.com/page/c/b/4/c0361j0fab4.html')
    #keywordSearch(1,"simpsons full episode")


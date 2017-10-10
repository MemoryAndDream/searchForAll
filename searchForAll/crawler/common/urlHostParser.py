#coding=utf8
import re
from urlparse import urlparse
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

topHostPostfix = (
    '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me', '.mobi',
    '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn', '.net.cn',
    '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag', '.net.ag',
    '.org.ag', '.am', '.asia', '.at', '.be', '.com.br', '.net.br',
    '.bz', '.com.bz', '.net.bz', '.cc', '.com.co', '.net.co',
    '.nom.co', '.de', '.es', '.com.es', '.nom.es', '.org.es',
    '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in',
    '.ind.in', '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms',
    '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz',
    '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw',
    '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', ".com.hk", '.xyz', 'top')


def parser(url):
    regx = r'[^\.]+(' + '|'.join([h.replace('.', r'\.') for h in topHostPostfix]) + ')$'
    pattern = re.compile(regx, re.IGNORECASE)
    parts = urlparse(url)
    host = parts.netloc
    m = pattern.search(host)
    res =  m.group() if m else host
    return "unkonw" if not res else res


def make_links_absolute(page,baseUrl): #将前100条链接修正
    def joinUrl(matched):

        return urljoin(baseUrl,matched.group("url"))
    endIndex=0
    if baseUrl.endswith('/'):
        baseUrl=baseUrl[:-1]
    for i in range(500):
        pattern = re.compile('''(href|src)\s*=\s*("|')?(?P<url>.*?)("|'|>)''')#居然没有引号也是可以的。。。
        reob= pattern.search(page,endIndex)
        if not (reob and reob.group('url')):
            if i==0: print 'no match url in page'
            #
            #print page
            break
        endIndex = reob.end("url")
        url = reob.group('url')
        if url.startswith('http'):continue
        if url.startswith('//'):continue
        startIndex = reob.start("url")
        if url.startswith('/'):
            page = page[:startIndex]+baseUrl+page[startIndex:]
        else:
            page = page[:startIndex] + baseUrl +'/'+ page[startIndex:]


        #print endIndex
        #否则判断是/还是 开头
        #print reob.start("url"),reob.end("url")
    return  page



if __name__=='__main__':
    print parser('https://www.google.com.hk/search?client=aff-cs-360chromium&hs=TSj&q=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&oq=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&gs_l=serp.3...74418.86867.0.87673.28.25.2.0.0.0.541.2454.2-6j0j1j1.8.0....0...1c.1j4.53.serp..26.2.547.IuHTj4uoyHg')
    url ='https://www.google.com.hk/search?client=aff-cs-360chromi'
    print '/'.join(url.split('/')[:3])
    print
    print urljoin("http://www.baidu.com", "abc.html")
    print urljoin("https://www.coder4.com/archives/2674", "../abc.html")
    print urljoin("http://www.baidu.com/xxx", "./../abc.html")
    print urljoin("https://www.coder4.com/archives/2674", "abc.html?key=value&m=x")
    print make_links_absolute('''<br><a href="/45215" title="搜索盘" class="gray" 布&nbsp; • &nbsp;<a target="_blank" href="/u/bd-1464156243">北欧战<a href="/079c09153225d7c6ae4cdab9e777a4bd2f042600">PES 2018犯浪荡爷的主页</a></span></p></div><div cla''','https://www.coder4.com' )
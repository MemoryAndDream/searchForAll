#coding=utf8
import importlib

SITES = {
    'baidu.com' : 'baidu',
'bing.com' : 'bing',
     
}#域名和模块对应关系

mo =importlib.import_module('.'.join(["crawler",'extractors','baidu']))

print mo.test()
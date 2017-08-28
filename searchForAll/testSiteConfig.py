#coding=utf8
import importlib

mo =importlib.import_module('.'.join(["crawler",'extractors','baidu']))

print mo.process("https://www.baidu.com/s?wd=%E5%88%86%E9%9A%94%E5%8F%B7")
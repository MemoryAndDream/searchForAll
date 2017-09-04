#coding=utf8
import importlib

mo =importlib.import_module('.'.join(["crawler",'extractors','google']))

print mo.process("https://www.google.co.kr/search?q=%E8%B0%B7%E6%AD%8C%E7%88%B8%E7%88%B8&start=40")
#coding=utf8
import importlib

mo =importlib.import_module('.'.join(["crawler",'extractors','universal']))

print mo.process("300",'1','mj0351')
#coding=utf8
import importlib
if __name__=='__main__':
    print 'test'
    mo =importlib.import_module('.'.join(["crawler",'extractors','universal']))
    print mo.process("mom",'1','panduoduo')
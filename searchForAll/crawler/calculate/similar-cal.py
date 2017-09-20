#coding=utf8

'''
目标： 基于搜索结果的聚类
分词, 词语重要性反比与出现频率

'''

#输入response
#字典是无序的。。所以顺序早就不对了 应该从字少的排起？ 然后每次将分数大于平均分一定倍数的全部加入队列

import jieba
import re


def splitWords(a):#传入所有标题构成的数组
	b=[]
	words = {}
	for i in range(len(a)):
		b.append([])
		if 'unicode' in str(type(a[i])):a[i] = re.sub(u'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", a[i])
		else:a[i] = re.sub(u'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "".decode("utf8"), a[i].decode('utf8'))
		rs=jieba.cut(a[i])
		#b.append("/ ".join(rs))
		for word in rs:

			#word=word.encode('utf8')
			if words.get(word):
				words[word]+=1
			else:
				words[word]=1
			b[i].append(word)

	for k,v in words.items():
		print  k,v

	return b,words



#感觉一个字的词比较没有意义 所以还应该乘以词字数 除以出现系数 这里考虑标题长度
def compareWords(words1,words2,words):
	sumScore=0
	for word in words1:
		if word in words2:
			sumScore += len(word)*1.0/words[word]
			print word,len(word)*1.0/words[word]
	return sumScore/len(words2)


def sortBySimilar(inputDicts,key):
#先不管字多少  过滤条件应该是固定前几名还是和平均值比较？ 固定的问题就是要精确一次只能pop一个，否则第二名容易差距很大，所以可以结合一下
	afterSort = []
	beforeSort=[]
	for i in range(len(inputDicts)):
		beforeSort[i] = inputDicts[i].get(key,'')
	print [v for k,v in beforeSort.items()]
	b,words = splitWords([v for v in beforeSort])  #输出切割后的标题数组
	print b,words
	opa=[]
	for i in range(len(b)):
		opa.append([i,b[i]])

	while len(opa)>3:
		sample = opa[0]
		afterSort.append(inputDicts[sample[0]])

		scores=[]
		for a in  opa[1:]:
			scores.append(compareWords(sample[1],a[1],words))


		opa.pop(0)





	pass




inputDicts = [{'url': u'https://detail.tmall.com/item.htm?id=524137711102', 'source': 'tmall', 'info': u'\u4ef7\u683c<em>42.80</em>\u5143 \u8d2d\u4e70\u6570\u91cf<em>3\u4eba\u4ed8\u6b3e</em>', 'imglink': u'//g-search2.alicdn.com/img/bao/uploaded/i4/i4/2678248660/TB26p7rlXXXXXXbXpXXXXXXXXXX_!!2678248660.jpg', 'title': u'\u3010\u7279\u4ef7\u3011\u65fa\u4ed4\u725b\u5976\u590d\u539f\u4e73\u8c03\u5236\u4e73\u5927\u5bb6\u5ead\u53f7\u513f\u7ae5\u725b\u5976125ML*28\u76d21\u6708\u4ea7-\u5929\u732b'}, {'url': u'https://detail.tmall.com/item.htm?id=557199790117', 'source': 'tmall', 'info': u'\u4ef7\u683c<em>38.00</em>\u5143 \u8d2d\u4e70\u6570\u91cf<em>0\u4eba\u4ed8\u6b3e</em>', 'imglink': u'//g-search1.alicdn.com/img/bao/uploaded/i4/i3/3368043109/TB2c56jXsiCJuJjy1XcXXcbAXXa_!!3368043109.jpg', 'title': u'\u3010\u6728\u5b50\u5e97\u3011\u65fa\u65fa125ml*20\u76d2\u4e00\u7bb1\u65fa\u4ed4\u725b\u5976\u5bb6\u5ead\u88c5\u590d\u539f\u4e73\u513f\u7ae5\u65e9\u9910\u5976-\u5929\u732b'}, {'url': u'https://detail.tmall.com/item.htm?id=529536249469', 'source': 'tmall', 'info': u'\u4ef7\u683c<em>99.99</em>\u5143 \u8d2d\u4e70\u6570\u91cf<em>9\u4eba\u4ed8\u6b3e</em>', 'imglink': u'//g-search3.alicdn.com/img/bao/uploaded/i4/i1/2854248831/TB2T.VeoVXXXXcmXpXXXXXXXXXX_!!2854248831.jpg', 'title': u'\u65fa\u65fa\u65fa\u4ed4\u725b\u5976\u590d\u539f\u4e73245ml*24\u7f50\u88c5\u7eff\u94c1\u7f50\u82f9\u679c\u5473\u4e73\u996e\u6599\u6574\u7bb1\u4fc3\u9500-\u5929\u732b'}]

sortBySimilar(inputDicts,'title')
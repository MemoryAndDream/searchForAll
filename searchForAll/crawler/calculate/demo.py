#coding=utf8
import jieba
import re
a=[]#输入str类型
a.append('无钢圈蕾丝可爱蝴蝶结少女士文胸套装调整型聚拢胸罩学生内衣薄款')
a.append('蕾丝内衣女套装少女文胸聚拢收副乳性感防下垂上托无钢圈调整胸罩')
a.append('时尔菲无钢圈聚拢文胸薄款抹胸防走光内衣调整型胸罩')
a.append('赠同款内裤】夏季超薄内衣无钢圈文胸性感透明胸罩三角杯bra套装 清新绿 M码(适合75=34ABC杯)')
a.append('新款特价诗婷内衣专柜正品加厚聚拢FA5438/薄杯FC5440大罩杯文胸')
a.append('体会内衣 奢华刺绣 中低腰收腹提臀 纯色刺绣美体塑身女式三角裤')
a.append('新款多种交叉美背内衣性感聚拢无痕无钢圈调整型小胸加厚5cm文胸')
a.append('丹皮尼 女式内裤夏季新款凉爽透气女士性感内衣低腰蕾丝透明三角裤')
a.append('无钢圈文胸聚拢上托小胸罩日系少女学生棉质无磁过安检肤色内衣女')
a.append('MI文胸套装女内衣性感蕾丝聚拢文胸深V调整型小胸品牌收副乳')
a.append('霏慕 雪纺刺绣女士性感睡衣优雅气质吊带睡裙缎面蕾丝诱惑情趣内衣睡袍女 粉色')
a.append('透明的影行内衣带引型带肩带透明肩带隐形吊带磨砂内衣带文胸带子')
a.append('安莉芳女士内衣 聚拢蕾丝边性感文胸 U型3/4立体软棉厚模杯胸围小胸EB1908 天蓝 75B')
a.append('透明的影行内衣带引型带肩带透明肩带隐形吊带磨砂内衣带文胸带子')
a.append('隐形文胸沙滩裙抹胸内衣聚拢无肩带加厚胸贴透气')

a.append('久慕雅黛性感透明睡衣睡裙夏女蕾丝吊带家居服诱惑网纱情趣内衣女 含丁字裤 西瓜红')
a.append('迪奥eddadior无钢圈文胸套装 透气条纹可拆卸无钢圈胸罩女 调整侧收副乳聚拢女士内衣 黑色(单文胸) 80B/36B尺码偏小，请加大一码')

a.append('诗媚儿无钢圈聚拢文胸调整型女士内衣蕾丝性感小胸收副乳深V无痕女士胸罩 黑色 38/85B(薄款1CM）')
a.append('2016新款豪门专柜正品内衣M364121女士磨毛弹力护膝v领保暖套装')
a.append('曼妮芬性感光面调整型内衣无钢圈聚拢文胸舒适无痕收副乳女士胸罩')
words={}


def splitWords():
	b=[]

	for i in range(len(a)):
		b.append([])
		a[i] = re.sub(u'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "".decode("utf8"), a[i].decode('utf8'))
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

	return b



#感觉一个字的词比较没有意义 所以还应该乘以词字数 除以出现系数
def compareWords(words1,words2):
	sumScore=0
	for word in words1:
		if word in words2:
			sumScore += len(word)*1.0/words[word]
			print word,len(word)*1.0/words[word]
	return sumScore/len(words2)
	pass

b = splitWords()
print 'start compare'
print compareWords(b[1],b[2])
print compareWords(b[3],b[4])
print compareWords(b[5],b[6])
print compareWords(b[7],b[9])
print compareWords(b[0],b[8])

'''结巴分词第一次载入需要1s，后面我为啥load失败了？'''





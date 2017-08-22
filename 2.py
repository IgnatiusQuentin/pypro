#爬取百度百科内容，并输出词云
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request as request
import re

#定义得到网页源码方法
def get_Html(url):
	#headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' } 
	#设置头文件，防止被墙
	#req=request.Request(url, headers=headers) 
	html=urlopen(url)
	txt=BeautifulSoup(str(html.read().decode('utf-8')),'lxml')
	return txt


#输入网页↓
html1=get_Html(input('please enter the web: '))
#得到网页源码↓
div=html1.find_all(name='div',attrs={"label-module": "para"})
#清除图片干扰项↓
descrip=re.compile(r'<div class="description">.*?</div>',re.S)
txt=descrip.sub('',str(div))
#清除网页源代码中的标签↓
dr = re.compile(r'<[^>]+>',re.S)
dd = dr.sub('',str(txt))
#清除文字中的空格
no_space_txt=re.sub(r'\s+','',dd)



with open('1.txt','w+',encoding='utf-8') as f:
	f.write(str(dd)+"\n")
	f.close



#python词云代码:
#coding:utf-8
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import jieba
import numpy as np
from PIL import Image

#读入背景图片
image = np.array(Image.open("3.png"))

#读取要生成词云的文件
file = open('1.txt','r',encoding='utf-8').read()

#通过jieba分词进行分词并通过空格分隔
wordlist = jieba.cut(file, cut_all = True)
split = " ".join(wordlist)

#生成词云
my_wordcloud = WordCloud(font_path = 'C:/Users/Windows/fonts/simkai.ttf',#设置字体格式，如不设置显示不了中文
).generate(split) 


# 根据图片生成词云颜色
image_colors = ImageColorGenerator(image)
#my_wordcloud.recolor(color_func=image_colors)

# 以下代码显示图片
plt.imshow(my_wordcloud)
plt.axis("off")
plt.savefig('test.png')
plt.show()








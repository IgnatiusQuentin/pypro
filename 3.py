#爬取豆瓣电影评价内容(py3.6.1)
#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
Author:Ignatius
Date:2017/8/12(Final Version)
'''

'''实现过程：
1、获取目标网页内容=get_html
2、输入名称，得到栏目评论第一页=get_first_page
3、从第一页得到评论数目=comment_num
4、在单页得到评论=match_comment
5、得到所有评论页地址=get_page_list
6、循环每一页评论，并输出到txt=out_txt
7、生成词云=word_cloud
8、利用main()将所有内容联系起来
'''
from urllib.request import urlopen
import urllib.request as request
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import jieba
import numpy as np
from PIL import Image
import time
from urllib.parse import quote
import  string

#获取网页内容'''已完成'''
def get_html(subject):
	headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0' } 
	#设置头文件，防止被墙
	req=request.Request(subject, headers=headers) 
	html=urlopen(req)
	txt=BeautifulSoup(str(html.read().decode('utf-8')),'lxml',fromEncoding="gb18030")
	return txt

#输入名称，得到栏目评论主页(第一页)地址'''已完成'''
def get_first_page(item):
	#得到作品相应搜索页
	item=re.sub(r' ','+',item)
	origin_web='https://www.douban.com/search?q='
	url=origin_web+str(item)
	url = quote(url,safe = string.printable)
	print('Downloading:'+str(url))
	txt1=get_html(url)
	urllist=txt1.find_all(name='h3')
	details=txt1.find_all(name='div',attrs={"class": "content"})
	n=1
	for detail in details:
		print(str(n)+'\n'+'=========================================='+'\n'+detail.text+'\n'+detail.text+'\n'+'==========================================')
		n+=1
	num=input('please enter the work you want:  ')
	urls=[]
	#将所有url形成列表
	for url in urllist:
		urls.append(url.a['href'])
	html=urls[int(num)-1]
	website=urlopen(html).url
	comment_page=website+'collections'
	return comment_page


#获取评论数量'''已完成'''
def comment_num(page_url):
	txt=get_html(page_url)
	#得到评论数目
	numinfo=txt.find_all(name='h2')
	num = re.findall('\d+',str(numinfo))
	return int(num[1])



#单页获取评论'''已完成'''
def match_comment(page_url):
	txt=get_html(page_url)
	comlist=txt.find_all(name='td',attrs={"valign": "top"})
	comlist2=BeautifulSoup(str(comlist),'lxml').find_all(name='p')
	pattern=re.compile(r'<p class="pl">.*?</p>',re.S)
	comlist3=pattern.sub('',str(comlist2))
	#清除评论中的标签↓
	dr = re.compile(r'<[^>]+>',re.S)
	dd = dr.sub('',str(comlist3))
	#清除评论中空格↓
	no_space_txt=re.sub(r'\s+','\n',dd)
	#清除评论中的标点↓
	no_pun_txt=re.sub(r'[,\[\]]','\n',no_space_txt)
	#清除评论中的空行↓
	perfect_txt=re.sub(r'\n+','\n',no_pun_txt)
	return perfect_txt

def get_page_list(name):
	#得到第一页
	page_url=get_first_page(name)
	#得到评论总页数
	num=comment_num(page_url)
	page_num=num//20
	print('\n\n========================================\nThere are  '+str(page_num+1)+'  pages')
	time_may=page_num//60
	if time_may>=1:
		print('Estimated time to download all comments is  '+str(time_may)+'  minutes\n========================================')
	else:
		print('Estimated time to download all comments is within 1 minute\n========================================')
	page_list=[]
	#获取所有评论页面网址
	for i in range(0,page_num+1):
		page_list.append(page_url+'?start='+str(i*20))
	return page_list



#将所有页面评论获取并保存在txt中
def out_txt(page_list,file_name):
	with open (file_name+'.txt','w+',encoding='utf-8') as f:
		n=1
		for page in page_list:
			print('Accessing page '+str(n))
			n+=1
			txt=match_comment(page)
			time.sleep(1)
			f.write(str(txt))
			f.write('\n\n')
		f.close
	print('Forming the wordcloud')

def word_cloud(file_name):#'''未完成'''
	#读入背景图片
	#image = np.array(Image.open("3.png"))

	#读取要生成词云的文件
	file = open(file_name+'.txt','r',encoding='utf-8').read()

	#通过jieba分词进行分词并通过空格分隔
	wordlist = jieba.cut(file, cut_all = True)
	split = " ".join(wordlist)
	my_wordcloud = WordCloud(font_path = 'C:/Users/Windows/fonts/simkai.ttf').generate(split) 
	'''my_wordcloud = WordCloud(
	background_color='white', # 设置背景颜色
	mask = image, # 设置背景图片
	max_words = 2000,  # 设置最大现实的字数
	#stopwords = STOPWORDS,  # 设置停用词
	font_path = 'C:/Users/Windows/fonts/simkai.ttf',#设置字体格式，如不设置显示不了中文
	max_font_size = 40,    # 设置字体最大值
	random_state = 42,     # 设置有多少种随机生成状态，即有多少种配色方案
	scale=1.5  #按比例放大(貌似没什么用)
	).generate(split)
	
	# 根据图片生成词云颜色
	image_colors = ImageColorGenerator(image)
	#my_wordcloud.recolor(color_func=image_colors)
	'''
	# 以下代码显示图片
	plt.imshow(my_wordcloud)
	plt.axis("off")
	plt.savefig(file_name+'.png')
	plt.show()

def main():
	file_name=input('please enter the name of the work:  ')
	page_list=get_page_list(file_name)
	out_txt(page_list,file_name)
	word_cloud(file_name)


main()
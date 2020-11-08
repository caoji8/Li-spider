#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 19:00
# @Author  : LLY
# @File    : text.py
print('12345人评价'[:-3])
import re
all='导演:陈凯歌KaigeChen主演:张国荣LeslieCheung张丰毅FengyiZha...|1993中国大陆香港剧情爱情同'
reg=re.compile('导演:|主演:')
info=reg.sub('|',all).split('|')[1:]
info.insert(1,'nihao')
print(info)
import operator
x=[{'a':1},{'b':2},{'c':3},{'d':4},{'e':5},{'f':6},{'g':7}]
def getKey(x):
    for k,v in x.items():
        return v
sorted_x=sorted(x,key=lambda e:getKey(e),reverse=True)
print(sorted_x)

# import hashlib
#
# str_start = '123546'
# print(str_start.isdigit())
#
# import re
#
# start = 'av123456'
# print(re.search(r'^av(\d+)/*', start).group(1))
#
# title = '"U::::u/\ib?\\di*."<>|'
# print(re.sub(r'[\/\\:*?"<>|.]', '', title))
#
# entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
# appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
#
# print(appkey, sec)
#
# print(''.join([chr(ord(i) + 2) for i in entropy[::-1]]))
# item = []
# for i in entropy[::-1]:
#     item.append(chr(ord(i) + 2))
#
# print(''.join(item).split(":"))
#
# appkey = 1
# cid = 2
# quality = 3
# params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
# print(params)
# chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
# print(chksum)
"""
import sys
import urllib
print(sys.path[1])
import os
print(os.getcwd())

title='慢慢喜欢你1'
path=os.path.join(os.getcwd(),'bilibili_video1',title)
print(path)

print(os.path.exists(path))
# os.makedirs(path)
"""

"""
进度条...
    @blocknum #数据块数
    @blocksize #单个数据块大小
    @totalsize #总共数据大小
"""
# while True:
#     try:
#         x=int(input('输入数字'))
#         break
#     except ValueError:
#         print('输入错误')

# from http.cookiejar import CookieJar
from http.cookiejar import MozillaCookieJar
from urllib import request
from urllib.parse import urlencode
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

CookieJar = MozillaCookieJar('cookie.txt')
hander = request.HTTPCookieProcessor(CookieJar)
opener = request.build_opener(hander)

data={

}
login_url='http://www.baidu.com'
req=request.Request(login_url,data=urlencode(data).encode('utf-8'),headers=headers)
opener.open(req)
CookieJar.save(ignore_discard=True)

str='中国 大学'
if str.startswith('中国'):
    print(str.replace('中国','').strip())


list_info=['python','c++','java','csharp']
for index,info in enumerate(list_info):
    print(index,info)

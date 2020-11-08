import requests
import json
import re

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'acw_tc=76b20ffc15536514820815291e59814f375891fbd81a3190ea2e4bef3bb853; token=dnaaabqcb5lw7wfj1gnbg; auth=0102E14FB6BEE9B3D608FEE1B77A20F2B3D6080016350078002D002D006100670032006F006400700074006E006D00780033006600780077007A006D006C00610000012F00FFE9FADC17239C4CC705D9139267FD90EEB7A65D0D',
#     'Host': 'mooc.icve.com.cn',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36'
#
# }
#
# url = 'https://mooc.icve.com.cn/design/process/editList?courseOpenId=wnnwargq24nomdiamckfq'
# re = requests.get(url, headers=headers)
# print(re.text)

file_path=r'/home/hadoop/桌面/pycharmwork/liuwork/课程讨论.txt'
fp=open(file_path,'w',encoding='utf-8')

with open(r'/home/hadoop/桌面/pycharmwork/liuwork/test1.json','r',encoding='utf-8')as re:
    pydata=json.load(re)
    print(pydata)


for list in pydata.get('list'):
    fp.write(list['name']+'\n\n')
    if 'topics' in list.keys() and list.get('topics')!=[]:
        for topics in list.get('topics'):
            fp.write('--------------------------------------------\n')
            fp.write(' '+topics['name']+'\n')
            for cell in topics.get('cells'):
                fp.write('\t'+cell['cellName']+'\n')
                for celltype in cell.get('childNodeList'):
                    if celltype['categoryName']=="讨论":
                        fp.write('\t\t'+celltype.get('cellContent').replace('<p>','').replace('</p>','')+'\n\n')#这有问题 看test.py
fp.close()




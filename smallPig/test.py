import os
import json
from lxml import html
import pandas as pd
import csv

filepath=os.getcwd()+r"\fangzi"
filecsv=os.getcwd()
flag=True
for file in os.listdir(filepath):
    pathall=os.path.join(filepath,file)
    with open(pathall,'r',encoding='utf-8')as f:
        reqhtml=f.read()

        # 条件 地点
        selector = html.fromstring(reqhtml)
        position = selector.xpath('//div[@class="pho_info"]/p/@title')[0]  # 地点
        price = selector.xpath('//div[@class="bg_box"]//div[@class="day_l"]/span/text()')[0]  # 价格

        photo = len(selector.xpath('//ul[@class="detail-thumb-nav"]/li/img/@data-src'))  # 照片
        # 各性描述
        personSay = ''.join(selector.xpath(
            '//div[@class="box_white clearfix detail_intro_item"]//div[@class=" intro_item_content"]/p/text()')).replace('\r','').replace('\n','').replace(' ','')
        # 屋内情况
        indoorInfo = ''.join(selector.xpath(
            '//div[@class="box_gray clearfix detail_intro_item"]//div[@class=" intro_item_content"]/p/text()')).replace('\r','').replace('\n','').replace(' ','')

        condition = selector.xpath('//ul[@class="pt_list clearfix"]/li/text()')
        noCondition = {'不适宜': []}
        yesCondition = {'适宜': []}
        for text in condition:
            if ' ' in text:
                if text.strip() != '':
                    yesCondition['适宜'].append(text.strip())
            else:
                noCondition['不适宜'].append(text)

        # 房东姓名
        lorderName = ''.join(selector.xpath('//a[@class="lorder_name"]/@title'))
        # 房东性别
        lorderSex = ''.join(selector.xpath('//div[@class="js_box clearfix"]//h6/span/@class')[0])
        if lorderSex == 'member_boy_ico':
            lorderSex = 'Man'
        else:
            lorderSex = 'Woman'
        commentName = selector.xpath('//h6/span[@class="col_pink"]/text()')
        commentText = selector.xpath('//div[@class="dp_box clearfix mt_10"]//text()')
        s = [x.strip().replace(' ', '').replace('\n', '').replace('\r', '') for x in commentText if x.strip() != '']
        index = []

        for num, value in enumerate(s):
            if value in commentName:
                index.append(num)
        commentContext = []  # 评论

        for k, v in enumerate(index):
            listemp = []
            if k == len(index) - 1:
                break
            for listInfo in range(index[k], index[k + 1]):
                listemp.append(s[listInfo])
                commentContext.append(listemp)

        # [0, 4, 10, 16, 22, 28, 34, 40, 46, 52, 59, 65, 71, 75, 81, 87, 93, 99, 105, 111]
        # 评分项
        viewTitle = selector.xpath('//*[@id="comment_box"]/div/ul/li/span/text()')

        if viewTitle == []:
            viewTitle = ['整洁卫生', '描述相符', '交通位置', '安全程度', '性价比']
        # 分数
        viewSorce = selector.xpath('//*[@id="comment_box"]/div/ul/li/text()')
        if viewSorce == []:
            viewSorce = ['暂无', '暂无', '暂无', '暂无', '暂无']
        # 综合分数
        dictView = {}
        for T, S in zip(viewTitle, viewSorce):
            dictView[T] = S

        scoreAvg = selector.xpath('//em[@class="score-rate"]/text()')
        if scoreAvg == []:
            scoreAvg = ['暂无']
        dictCommtent = {}
        for listComm in commentContext:
            dictCommtent[listComm[0]] = listComm[1:]

        dictData = {
            '地点': position,
            '价格': price,
            '照片': photo,
            '各性描述': personSay,
            '屋内情况': indoorInfo,
            '不适宜': ''.join(noCondition['不适宜']),
            '适宜': ''.join(yesCondition['适宜']),
            '房东姓名': lorderName,
            '房东性别': lorderSex,
            '综合分数': scoreAvg[0]
        }
        infoDict = {}
        for k, v in dictData.items():
            infoDict[k] = v
        for k, v in dictView.items():
            infoDict[k] = v
        with open(r'F:\ProgramWork\PyCharmProjects\smallPig\sps4.csv', 'a', encoding='gbk', errors='ignore',
                  newline='')as fc:
            if flag:
                keys = list(infoDict.keys())
                writer = csv.writer(fc, delimiter=',')
                writer.writerow(keys)
                values = list(infoDict.values())
                writer.writerow(values)
                flag = False
            else:
                writer = csv.writer(fc, delimiter=',')
                values = list(infoDict.values())
                writer.writerow(values)
                if not dictCommtent=={}:
                    writer.writerow(dictCommtent.keys())
                    writer.writerow(''.join(i) for i in dictCommtent.values())




    # def saveCsv(self, infoDict):
    #     with open(r'F:\ProgramWork\PyCharmProjects\smallPig\sps.csv', 'a', encoding='gbk', errors='ignore',
    #               newline='')as fc:
    #         if self.flag:
    #             keys = list(infoDict.keys())
    #             writer = csv.writer(fc, delimiter=',')
    #             writer.writerow(keys)
    #             values = list(infoDict.values())
    #             writer.writerow(values)
    #             self.flag = False
    #         else:
    #             writer = csv.writer(fc, delimiter=',')
    #             values = list(infoDict.values())
    #             writer.writerow(values)





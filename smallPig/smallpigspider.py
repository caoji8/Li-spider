import csv
import random
import time
import requests
from lxml import html
import re

class SPS():
    def __init__(self):
        self.listUrl = []
        self.flag = True
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            ,
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
            , 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
            , 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'
            ,
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
            ,
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.40'
            ,
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'
            ,
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'
            , 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'
            , 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            ,
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16']
        self.referer = [
            'http://bj.xiaozhu.com/search-duanzufang-p2-0/'
            , 'http://bj.xiaozhu.com/search-duanzufang-p4-0/'
            , 'http://bj.xiaozhu.com/search-duanzufang-p3-0/'
            , 'http://bj.xiaozhu.com/search-duanzufang-p6-0/'
            , 'http://bj.xiaozhu.com/search-duanzufang-p5-0/'
            , 'http://bj.xiaozhu.com/search-duanzufang-p7-0/'
            , 'http://bj.xiaozhu.com/'
            , 'http://bj.xiaozhu.com/'
            , 'http://cd.xiaozhu.com/'
            , 'http//xa.xiaozhu.com/'
            , 'http//sh.xiaozhu.com/'
            , 'http://xa.xiaozhu.com/search-duanzufang-p2-0/ '
            , 'http://sh.xiaozhu.com/search-duanzufang-p4-0/'
            , 'http://sh.xiaozhu.com/search-duanzufang-p3-0/'
            , 'http://xa.xiaozhu.com/search-duanzufang-p11-0/'
            , 'http://sh.xiaozhu.com/search-duanzufang-p5-0/'
            , 'http://xa.xiaozhu.com/search-duanzufang-p10-0/'
            , 'http://cd.xiaozhu.com/search-duanzufang-p4-0/'
            , 'http://sh.xiaozhu.com/search-duanzufang-p3-0/'
            , 'http://xa.xiaozhu.com/search-duanzufang-p9-0/'
            , 'http://cd.xiaozhu.com/search-duanzufang-p5-0/'
            , 'http://cd.xiaozhu.com/search-duanzufang-p7-0/'
        ]

    def reqMain(self, url):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "abtest_ABTest4SearchDate=b; gr_user_id=c95e7655-706a-4dc5-97e1-f85aefd6511f; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_cs1=N%2FA; grwng_uid=088ec835-f5ab-4f04-abf0-a92052808fab; _uab_collina=155893601956385064475774; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id=1b0b387f-a388-4db4-913f-97fb65de9c96; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_sid_with_cs1=1b0b387f-a388-4db4-913f-97fb65de9c96; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id_1b0b387f-a388-4db4-913f-97fb65de9c96=true; xzuuid=c1fc62af; TY_SESSION_ID=24cfd18f-26c9-4052-aac2-d7bfaaba9682; Hm_lvt_92e8bc890f374994dd570aa15afc99e1=1558956728,1558957950,1558959451,1558959623; rule_math=f2bu3qe1kcu; Hm_lpvt_92e8bc890f374994dd570aa15afc99e1=1558959624",
            "Host": "bj.xiaozhu.com",
            "Referer": "http://bj.xiaozhu.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        try:
            # time.sleep(2)
            req = requests.get(url=url, headers=headers)
            if req.status_code == 200:
                print('获取成功！')
                req.encoding = 'utf-8'
                return req.text
        except Exception as ex:
            print(ex)

    def getReqFangzi(self, url):
        reg = re.compile('/(\d+)\.html')
        num = reg.findall(url)[0]
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "abtest_ABTest4SearchDate=b; Hm_lvt_92e8bc890f374994dd570aa15afc99e1=1558935967; gr_user_id=c95e7655-706a-4dc5-97e1-f85aefd6511f; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id=0ed6eb9c-621b-430b-b6c4-58d8ea293c7b; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_sid_with_cs1=0ed6eb9c-621b-430b-b6c4-58d8ea293c7b; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_cs1=N%2FA; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id_0ed6eb9c-621b-430b-b6c4-58d8ea293c7b=true; grwng_uid=088ec835-f5ab-4f04-abf0-a92052808fab; xzuuid=ee9930e8; TY_SESSION_ID=9219422d-be1d-4bd8-99ef-11b25d369f57; _uab_collina=155893601956385064475774; rule_math=f2bu3qe1kcu; Hm_lpvt_92e8bc890f374994dd570aa15afc99e1=1558937664",
            "Host": "bj.xiaozhu.com",
            "Referer": random.choice(self.referer),
            "User-Agent": random.choice(self.ua),
            "X-Requested-With": "XMLHttpRequest",
            "X-Tingyun-Id": "uxh10gyAidI;r=937664438",
            "xSRF-Token": "d27538a7ea5c92790d003e71728784d0"
        }
        try:
            time.sleep(2)
            req = requests.get(url=url, headers=headers)
            if req.status_code == 200:
                print('获取成功')
                # req.encoding = req.apparent_encoding
                with open(r'F:\ProgramWork\PyCharmProjects\smallPig\fangzi1\{}.html'.format(num),'wb')as f:
                    f.write(req.content)
                print('写入成功')
                # return req.content
        except Exception as ex:
            print(ex)

    def paserFangzi(self, reqFanngziHtml):
        # 条件 地点
        selector = html.fromstring(reqFanngziHtml)
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
        with open(r'F:\ProgramWork\PyCharmProjects\smallPig\sps.csv', 'a', encoding='gbk', errors='ignore',
                  newline='')as fc:
            if self.flag:
                keys = list(infoDict.keys())
                writer = csv.writer(fc, delimiter=',')
                writer.writerow(keys)
                values = list(infoDict.values())
                writer.writerow(values)
                self.flag = False
            else:
                writer = csv.writer(fc, delimiter=',')
                values = list(infoDict.values())
                writer.writerow(values)
                if not dictCommtent=={}:
                    writer.writerow(dictCommtent.keys())
                    writer.writerow(''.join(i) for i in dictCommtent.values())

    def getNextUrl(self, reqHtml):
        selector = html.fromstring(reqHtml)
        nextUrl = selector.xpath('//a[@class="resule_img_a"]/@href')
        self.listUrl.append(nextUrl)

    def main(self):
        for numPage in [_ for _ in range(1, 4)]:
            urlMain = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(numPage)
            reqHtml = self.reqMain(urlMain)
            self.getNextUrl(reqHtml)
        for listurl in self.listUrl:

            for url in listurl:
                print('正在爬取：' + url)
                reqFanngzi = self.getReqFangzi(url)
                self.paserFangzi(reqFanngzi)
                # self.saveCsv(infoDict)


if __name__ == '__main__':
    sps = SPS()
    sps.main()

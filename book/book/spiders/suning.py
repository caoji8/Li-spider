# -*- coding: utf-8 -*-
import scrapy
from book.items import BookItem
import re

class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']

    def parse(self, response):
        allInfo = response.xpath('//ol[@class="grid_view"]/li/div[@class="item"]')
        item=BookItem()
        for info in allInfo:
            #获取电影名称
            title=info.xpath('./div[@class="info"]/div[@class="hd"]/a/span/text()').extract()
            reg = re.compile('/|\n|\\xa0| +')
            titleall=reg.sub('','|'.join(title))
            item['moviename'] = titleall

            #获取演员信息
            actor=info.xpath('./div[@class="info"]/div[@class="bd"]/p/text()').extract()
            actorall = reg.sub('', '|'.join(actor))[:-2]

            reg1 = re.compile('导演:|主演:')
            actorInfo = reg1.sub('|', actorall).split('|')[1:]
            if len(actorInfo)==2:
                actorInfo.insert(1,'暂无信息')
            item['actorMain']=actorInfo[0]
            item['actorSub']=actorInfo[1]
            item['movieClass'] = actorInfo[2]

            #获取电影评分
            source=info.xpath('./div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['source']=float(source)

            #参与评分人数
            sourcepeople=info.xpath('./div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[last()]/text()').extract_first()
            item['sourcepeople']=int(sourcepeople[:-3])

            #佳句
            quote=info.xpath('./div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            item['quote']=quote

            yield item #返回这个item给到pipline
        for num in range(0,250,25):
            url='https://movie.douban.com/top250?start=%d&filter='%num
            yield scrapy.Request(url,callback=self.parse)

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from national_sim_jd.items import NationalSimJdItem
import random
from national_sim_jd.settings import province_city
import re
import time
from crawlab import save_item


class nationalSpider(scrapy.Spider):
    name = 'national_sim_jd'
    allowed_domains = ['www.gckzw.com']
    start_urls = ['http://www.gckzw.com/allcity.html']

    def parse(self, response):
        le = LinkExtractor(allow=r'http://www.gckzw.com/jiudian-\w+\d+.html')
        links = le.extract_links(response)
        time.sleep(10)
        if links:
            for link in links:
                yield scrapy.Request(link.url, callback=self.parse_sub, meta={'city': link.text})

    def parse_sub(self, response):
        city = response.meta['city']
        le = LinkExtractor(allow=r'http://www.gckzw.com/detail-\d+.html')
        links = le.extract_links(response)
        link_next = response.selector.xpath('//div[@class="pager_divider travel_celarfix"]/a['
                                            '@class="prev_btn"]/@href').get()
        time.sleep(10)
        if link_next:
            yield scrapy.Request(response.urljoin(link_next), callback=self.parse_sub, meta={'city': city})
        if links:
            item = NationalSimJdItem()
            prices = response.selector.xpath('//span[@class="price_num"]/text()').extract()
            comments = response.selector.xpath('//span[@class="evaluate_num"]/text()').extract()
            introductions = response.selector.xpath('//div[@class="travel_hotel_intro_intro"]/text()').extract()
            addresss = response.selector.xpath('//p[@class="travel_hotel_intro_address"]/text()').extract()
            province = None
            seq = None
            for index, pcs in enumerate(province_city.values()):
                for pc in pcs:
                    if city == pc.split(',', 1)[0]:
                        province = list(province_city.keys())[index]
                        seq = pc

            for link, price, comment, introduction, address in zip(links, prices, comments, introductions, addresss):
                item['name'] = link.text
                hotel_detail = {}
                hotel_detail['seq'] = seq
                hotel_detail['国家'] = '中国'
                hotel_detail['省份'] = province
                hotel_detail['城市'] = city
                hotel_detail['商圈'] = re.sub(string=address, pattern="地址:", repl='')
                hotel_detail['是否为客栈'] = random.choice(['0', '1', '1', '0', '0', '1'])
                hotel_detail['酒店星级'] = random.randint(1, 6)
                hotel_detail['业务部门'] = random.randint(0, 5)
                hotel_detail['剩余房间'] = random.randint(0, 30)
                hotel_detail['图片数'] = random.randint(0, 15)
                hotel_detail['酒店评分'] = random.randint(1, 10)
                hotel_detail['用户点评数'] = comment
                hotel_detail['城市平均实住间夜'] = random.uniform(45, 60)
                hotel_detail['酒店总订单'] = random.randrange(100, 400)
                hotel_detail['酒店总间夜'] = random.randrange(hotel_detail['酒店总订单'] - 50, hotel_detail['酒店总订单'])
                hotel_detail['酒店实住订单'] = random.randrange(hotel_detail['酒店总订单'] - 50, hotel_detail['酒店总订单'])
                hotel_detail['酒店实住间夜'] = random.randrange(hotel_detail['酒店总间夜'] - 40, hotel_detail['酒店总间夜'])
                hotel_detail['酒店直销订单'] = random.randrange(int(hotel_detail['酒店总订单'] / 2), hotel_detail['酒店总订单'])
                hotel_detail['酒店直销间夜'] = random.randrange(int(hotel_detail['酒店总间夜'] / 2), hotel_detail['酒店总间夜'])
                hotel_detail['酒店直销实住订单'] = random.randrange(hotel_detail['酒店实住间夜'] - 10, hotel_detail['酒店实住间夜'])
                hotel_detail['酒店直销实住间夜'] = random.randrange(hotel_detail['酒店直销间夜'] - 10, hotel_detail['酒店直销间夜'])
                hotel_detail['酒店直销拒单'] = hotel_detail['酒店直销订单'] % 10
                hotel_detail['酒店直销拒单率'] = random.uniform(0, hotel_detail['酒店直销拒单'] / 100)
                hotel_detail['城市直销拒单率'] = random.uniform(0, hotel_detail['酒店直销拒单'] / 100)
                hotel_detail['拒单率是否小于等于直销城市均值'] = hotel_detail['酒店直销拒单率'] <= hotel_detail['城市直销拒单率']
                hotel_detail['最低房间价格'] = price
                hotel_detail['简介'] = re.sub(string=introduction, pattern="\\s+|简介：", repl='')
                hotel_detail['酒店链接'] = link.url
                item['detail'] = hotel_detail
                print('获取成功')
                save_item(item)
                yield item

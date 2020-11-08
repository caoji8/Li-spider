# -*- coding: utf-8 -*-
import scrapy
from ZotPhone.items import ZotphoneItem
import re
import time


class PhoneSpider(scrapy.Spider):
    name = 'Phone'
    allowed_domains = ['detail.zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_1.html']

    def parse(self, response):
        item = ZotphoneItem()
        # 一个页面
        data_list = response.selector.xpath('//div[@class and@data-follow-id]')
        for data_ in data_list:
            # 页面详情
            detail_list = []
            name = data_.xpath(
                './div[@class="pro-intro"]/h3/a[@target="_blank"and not(@class="try-link")]/text()').get()

            price = data_.xpath('./div[@class="price-box"]/span/b[@class="price-type"]/text()').extract()
            price_time = data_.xpath('./div[@class="price-box"]/span[@class="date"]/text()').extract()
            numbers = len(data_.xpath('./div[@class="pro-intro"]/ul[@class="param clearfix"]/*'))

            for num in range(1, numbers + 1):
                detail_temp = self.parse_detail(data_, str(num))
                detail_list.append(detail_temp)
            item["detail"] = detail_list
            mark = data_.xpath('./div[@class="pro-intro"]/div[@class="special clearfix"]/div/b/text()').extract()
            review_people = data_.xpath('./div[@class="pro-intro"]/div[@class="special clearfix"]/div/span/a/text('
                                        ')').extract()

            item['price'] = ''.join(price)
            item['price_time'] = ''.join(price_time)
            item["name"] = ''.join(name)
            item["mark"] = ''.join(mark)
            item['review_people'] = ''.join(review_people)
            yield item
        # next_page = response.selector.xpath('//div[@class="page-box"]/div[@class="pagebar"]/a['
        #                                     '@class="next"]/@href').extract()

        time.sleep(5)
        for next_num in range(1, 105):
            yield scrapy.Request(
                url='http://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_0_1_1_0_{}.html'.format(
                    str(next_num)),
                callback=self.parse)

    def parse_detail(self, data_, number):
        detail_temp = {}

        dt_key = data_.xpath('./div[@class="pro-intro"]/ul[@class="param clearfix"]/li[{}]/span/text()'.format(
            number)).extract()[0]
        dt_value_temp = [data_temp for data_temp in
                         data_.xpath('./div[@class="pro-intro"]/ul[@class="param '
                                     'clearfix"]/li[{}]/text('
                                     ')'.format(number)).extract() if not
                         data_temp.isspace()][0]

        dt_value = re.sub(string=dt_value_temp, pattern="\s+", repl='')
        dt_key = re.sub(string=dt_key, pattern="：", repl='')
        detail_temp[dt_key] = dt_value
        return detail_temp

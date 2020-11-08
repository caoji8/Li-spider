# -*- coding: utf-8 -*-
import scrapy
from exhibition.items import ExhibitionItem
import re
import copy
import random
import time


class DownloadhtmlSpider(scrapy.Spider):
    name = 'downloadhtml'
    allowed_domains = ['globalimporter.net', 'hm.baidu.com']
    start_urls = ['http://www.globalimporter.net/expo.asp']

    def parse(self, response):
        print(response.status, '主页')
        main_urls = response.selector.xpath('//div[@class="top"and@align="left"]/a[contains(@href,'
                                            '"expo_month.asp?")]/@href').extract()
        for url in main_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.sub_parse)
            # 使用yield才调度器会把请求对象给downloader

    def sub_parse(self, response):
        print(response.status, '每月')
        sub_urls = response.selector.xpath('//td[@align="left" and @valign="top"]/a[@href]/@href').extract()
        for url in sub_urls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.end_parse)

    def end_parse(self, response):
        print(response.status, '每页')
        end_urls = response.selector.xpath(
            '//table[@class="top" and@height and@cellspacing and@cellpadding]/tbody/tr/td/a['
            '@class="blue2"]/@href').extract()
        months = response.selector.xpath('//table[@class="top" and@height and@cellspacing and@cellpadding]/tbody/tr/td['
                                         '@valign="top" and@width]/text()').extract()
        if len(end_urls) == len(months):
            for url, month in zip(end_urls, months):
                yield scrapy.Request(url=response.urljoin(url), callback=self.detail_parse,
                                     meta={'month': copy.deepcopy(
                                         month)})

    def find_str(self, regx, str_, index, str2):
        regx_str = regx.findall(str_[0])
        if len(regx_str) is not 0:
            regx_str = regx.sub('', str2[index][0])
            return regx_str
        else:
            return None

    def detail_parse(self, response):
        print(response.status, '详情')
        item = ExhibitionItem()
        item['month'] = response.meta['month']
        # 展会标题
        item['zhtitle'] = response.selector.xpath('//td[@class="blue" and@background="images/left.gif"]/text('
                                                  ')').extract_first()
        double_data = response.selector.xpath(
            '//td[@align="left" and@class="top"]/a[@href and@class="blue2"]/text()').extract()
        # 展会类别
        try:
            item['zhcategory'] = double_data[0]
        except:
            item['zhcategory'] = None
            print(response.url)

        # 展会城市
        try:
            item['zhcity'] = double_data[1]
        except:
            item['zhcity'] = None
            print(response.url)

        split_data = response.selector.xpath('//td[@align="left" and@class="top"]/text()').extract()
        try:
            zhcountry_re = split_data[4]
            regx_country = re.compile('举办国家: (\S+)')
            # 参展国家(就是举办国)
            item['zhcountry'] = regx_country.match(zhcountry_re).group(1)

            zhname_re = split_data[7]
            regx_name = re.compile('展馆名称: (\S+)')
            # 展馆名称
            item['zhname'] = regx_name.match(zhname_re).group(1)
        except:
            item['zhcountry'] = None
            item['zhname'] = None
            print(response.url)
        time_data_str = response.selector.xpath('//td[@align="left" and@class="top"]/span[@class="hui"]/text('
                                                ')').extract_first()
        try:
            time_data_all = time_data_str.split('~')
            # 展会开始时间
            item['timestart'] = time_data_all[0]
            # 展会结束时间
            item['timeend'] = time_data_all[1]
        except:
            item['timestart'] = None
            item['timeend'] = None
            print(response.url)

        content_re = response.selector.xpath(
            '//td[@align and not(@background or@class or@width or@height or@valign or@bgcolor)]/text()').extract()
        regx_str = re.compile('\S+')
        content_lists = [regx_str.findall(str_) for str_ in content_re if len(regx_str.findall(str_)) is
                         not 0]

        for index, str0 in enumerate(content_lists):
            if len(str0) >= 2:
                content_lists[index] = [''.join(str0)]
        # 展会说明
        item['zhcontent'] = '@#@'.join(content[0] for content in content_lists)
        item['_id'] = item['month'] + '-' + str(time.time())
        if item['zhtitle'] is not None:
            yield item

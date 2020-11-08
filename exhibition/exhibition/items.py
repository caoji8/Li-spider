# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExhibitionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    zhtitle = scrapy.Field()
    zhname = scrapy.Field()
    zhcategory = scrapy.Field()
    zhcity = scrapy.Field()
    zhcountry = scrapy.Field()
    timestart = scrapy.Field()
    timeend = scrapy.Field()
    zhcontent = scrapy.Field()
    month = scrapy.Field()
    # image_urls=scrapy.Field()
    # images=scrapy.Field()


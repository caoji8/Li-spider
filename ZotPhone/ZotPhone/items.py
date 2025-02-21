# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZotphoneItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    price_time=scrapy.Field()
    mark = scrapy.Field()
    review_people = scrapy.Field()

    detail = scrapy.Field()

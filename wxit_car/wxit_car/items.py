# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WxitCarItem(scrapy.Item):
    name = scrapy.Field()
    factory = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    price = scrapy.Field()
    model = scrapy.Field()
    sale_equip_config = scrapy.Field()
    score_project = scrapy.Field()
    projects_detail = scrapy.Field()

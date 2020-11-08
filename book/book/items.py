# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    moviename = scrapy.Field()
    actorMain=scrapy.Field()
    actorSub=scrapy.Field()
    movieClass=scrapy.Field()
    source=scrapy.Field()
    sourcepeople=scrapy.Field()
    quote=scrapy.Field()
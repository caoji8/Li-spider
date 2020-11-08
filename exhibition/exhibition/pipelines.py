# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
from scrapy.pipelines.images import ImagesPipeline


class ExhibitionPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['db_data5']

    def process_item(self, item, spider):
        regx = re.compile('(\d+-\d+)-\d+')
        collection = regx.match(item['month']).group(1)
        myitem = self.db[collection]
        myitem.insert_one(item)

    def close_spider(self, spider):
        self.client.close()

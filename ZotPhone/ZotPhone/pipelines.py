# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ZotphonePipeline(object):
    def __init__(self):
        self.file=open('ZolPhone.json',mode='a',encoding='utf-8')

    def process_item(self, item, spider):
        dict_data={}
        dict_data['name']=item['name']
        dict_data['price']=item['price']
        dict_data['price_time']=item['price_time']
        dict_data['mark']=item['mark']
        dict_data['review_people']=item['review_people']
        dict_data['detail']=list(item["detail"])

        json.dump(fp=self.file,obj=dict_data,ensure_ascii=False)
        print("OK")
        self.file.write('\n')
        return item

    def close_spider(self, spider):
        self.file.close()

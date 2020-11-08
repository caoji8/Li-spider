# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
# class BookPipeline(object):
# #     def open_spider(self,spider):
# #         self.f=open(r'F:\ProgramWork\PyCharmProjects\book\book\spiders\test.csv','a',encoding='utf-8',newline='')
# #         headers=['moviename','actorMain','actorSub','movieClass','source','sourcepeople','quote']
# #         self.wither=csv.DictWriter(f=self.f,fieldnames=headers)
# #         self.wither.writeheader()
# #     def close_spider(self,spider):
# #         self.f.close()
# #     def process_item(self, item,spider):
# #         # lins=json.dumps(dict(item),ensure_ascii=False)#这里一定要转化成dict
# #         # self.f.write(lins)
# #         # self.f.write('\n')
# #         self.wither.writerow(item)
# #         return item
import pymysql
class BookPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='scrapyMysql',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def open_spider(self,spider):
        self.cursor.execute('DROP TABLE IF EXISTS doubantop250;')
        self.cursor.execute('create table doubantop250('
                            'moviename varchar (128),'
                            'actorMain varchar (128),'
                            'actorSub varchar (128),'
                            'movieClass varchar (128),'
                            'quote varchar (128),'
                             'source double (2,1),'
                            'sourcepeople int ,'
                            'timelocal timestamp '
                            ')')
    def process_item(self,item,spider):
        self.cursor.execute('insert into doubantop250 values (%s,%s,%s,%s,%s,%s,%s,%s)',
                            (item['moviename'],item['actorMain'],item['actorSub'],item['movieClass'],item['quote'],item['source'],item['sourcepeople'],None))
        self.connect.commit()
    def close_spider(self,spider):
        self.cursor.execute('alter table doubantop250  add id int(10) primary key AUTO_INCREMENT;')
        self.connect.commit()
        self.cursor.close()


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings

from twisted.enterprise import adbapi


class MySQLPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, cralwer):
        db_params = {
            'host': cralwer.settings['MYSQL_HOST'],
            'user': cralwer.settings['MYSQL_USER'],
            'passwd': cralwer.settings['MYSQL_PASSWORD'],
            'db': cralwer.settings['MYSQL_DBNAME'],
            'port': cralwer.settings['MYSQL_PORT'],
            'charset': cralwer.settings['MYSQL_CHARSET']
        }
        drool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(drool)

    def process_item(self, item, spider):
        print(item)
        query = self.dbpool.runInteraction(
            self.insert_data_to_mysql,
            item
        )
        query.addErrback(
            self.insert_err,
            item
        )
        return item

    @staticmethod
    def insert_data_to_mysql(cursor, item):
        insert_sql = """ 
                insert into car(`name`,`factory`,`type`,`price`,`level`,`model`,`sale_equip_config`,`score_project`,`projects_detail`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                """
        cursor.execute(insert_sql, (
            str(item['name']), str(item['factory']), str(item['type']), str(item['price']), str(item['level']),
            str(item['model']), str(item['sale_equip_config']), str(item['score_project']),
            str(item['projects_detail'])))

    @staticmethod
    def insert_err(failure, item):
        print(failure, '失败', item)

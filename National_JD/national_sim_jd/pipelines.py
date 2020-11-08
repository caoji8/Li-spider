# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from national_sim_jd.settings import mysqlconnect
import logging


class NationalSimJdPipeline(object):
    def __init__(self):
        print('连接数据库')
        self.connect = pymysql.connect(host=mysqlconnect['MYSQL_HOST'], db=mysqlconnect['MYSQL_DBNAME'],
                                       user=mysqlconnect['MYSQL_USER'],
                                       passwd=mysqlconnect['MYSQL_PASSWD'], charset='utf8', use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        datadetail = item['detail']
        try:
            # 插入数据
            self.cursor.execute(
                """insert into simjd(name,seq,county,province,city,address,isinn,grade,department,rooms,
                images,mark,comment,averagenights,totalorder,totalnights,realorder,realnights,directorder,
                directnights,directrealorder,directrealnights,directrejectorder,jddirectrejectorderrate,
                citydirectjectorderrate,lookjdcityrate,price,introduction,url)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['name'],
                 datadetail['seq'],
                 datadetail['国家'],
                 datadetail['省份'],
                 datadetail['城市'],
                 datadetail['商圈'],
                 datadetail['是否为客栈'],
                 datadetail['酒店星级'],
                 datadetail['业务部门'],
                 datadetail['剩余房间'],
                 datadetail['图片数'],
                 datadetail['酒店评分'],
                 datadetail['用户点评数'],
                 datadetail['城市平均实住间夜'],
                 datadetail['酒店总订单'],
                 datadetail['酒店总间夜'],
                 datadetail['酒店实住订单'],
                 datadetail['酒店实住间夜'],
                 datadetail['酒店直销订单'],
                 datadetail['酒店直销间夜'],
                 datadetail['酒店直销实住订单'],
                 datadetail['酒店直销实住间夜'],
                 datadetail['酒店直销拒单'],
                 datadetail['酒店直销拒单率'],
                 datadetail['城市直销拒单率'],
                 datadetail['拒单率是否小于等于直销城市均值'],
                 datadetail['最低房间价格'],
                 datadetail['简介'],
                 datadetail['酒店链接'],
                 ))
            # 提交sql语句
            self.connect.commit()
            print('存储成功')
        except Exception as error:
            # 出现错误时打印错误日志
            logging.warning(error)
        return item

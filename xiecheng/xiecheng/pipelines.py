# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class XiechengPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    # 打开数据库
    def __init__(self):
        # self.conn = pymysql.connect(ip,用户，密码，数据库，字符集)
        self.conn = pymysql.connect("127.0.0.1", "root", "wangjian","xiecheng",charset="utf8")
        print("-----------------------打开数据库-------------------------------")
        # 游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

class XiechenglvyouPipeline(MysqlPipeline):

    def process_item(self,item,spider):
        sql = "insert into products(classify_name,intor,scenic_spot_name,scenic_spot_stars,hotel_name,hotel_stars,days,price,scenic_spot_url) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (item["classify_name"],item["intor"],item["scenic_spot_name"],item["scenic_spot_stars"],item["hotel_name"],item["hotel_stars"],item["days"],item["price"],item["scenic_spot_url"])

        try:
            self.cursor.execute(sql,data)
            self.conn.commit()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~插入数据库~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except Exception as e:
            print("插入失败", e)
            self.conn.rollback()

        return item




    # def __init__(self):
    #     self.file = open("xiecheng.json","w",encoding="utf-8")
    # def process_item(self, item, spider):
    #     data = json.dumps(dict(item), ensure_ascii=False) + '\n'
    #     with open("xiecheng.json",'a',encoding="utf-8") as f:
    #         self.file.write(data)
    #     return item
    # def close_spider(self,spider):
    #     self.file.close()

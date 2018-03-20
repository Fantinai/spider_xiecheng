# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class XiechenglvyouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classify_name = scrapy.Field() #景点主题分类信息
    classify_url = scrapy.Field() #景点主题分类信息url

    scenic_spot_name = scrapy.Field() #1,景点名称
    scenic_spot_stars = scrapy.Field() #2,景点评分
    hotel_name  = scrapy.Field() #3,酒店
    hotel_stars  = scrapy.Field() #4,酒店评分
    days  = scrapy.Field() #5, 天数
    intor = scrapy.Field() #6, 简单介绍:
    price  = scrapy.Field()#7, 套餐价格:
    scenic_spot_url = scrapy.Field() #8景点详情url





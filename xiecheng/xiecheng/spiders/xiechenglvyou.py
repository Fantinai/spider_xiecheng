# -*- coding: utf-8 -*-
import scrapy
from xiecheng.items import XiechenglvyouItem
import time,re

class XiechenglvyouSpider(scrapy.Spider):
    name = 'xiechenglvyou'
    allowed_domains = ['weekend.ctrip.com']
    start_urls = ['http://weekend.ctrip.com/around/Beijing']

    def parse(self, response):
        #time.sleep(5)
        #html = response.text
        #with open("xiechengBeijing.html","w",encoding="utf-8") as file:
        #    file.write(html)
        print(response.url)
        #查找分类信息
        classify_list = response.xpath('//ul[@id="wc_list"]/li//div[@class="wc_link_title"]')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(len(classify_list))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #遍历分类信息
        for classifys in classify_list:
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #print(classifys)
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #创建item对象
            item = XiechenglvyouItem()

            # 查找分类信息名称
            classify_name = classifys.xpath('./a/@title').extract()[0]
            item["classify_name"] = classify_name
            print("~~~~~~~~~~~~%s~~~~~~~~~~~"%classify_name)

            #查找分类信息url
            classify_url = classifys.xpath('./a/@href').extract()[0]
            classify_url = "http://weekend.ctrip.com" + classify_url
            item["classify_url"] = str(classify_url)

            #测试查到的数据,分类信息名称,分类信息url
            '''
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(classify_url)
            print(classify_name)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            '''
            #到下一层继续取数据
            #yield item
            yield scrapy.Request(url=classify_url,callback=self.parse_second,meta={"data":item})

    def parse_second(self,response):
        #print("~~~~~~~~~~~~~~~~第二层爬取!~~~~~~~~~~~~~~~~~~~~~")
        #print(response.url)

        #获取页码地址
        page = response.xpath('//div[@class="pkg_page basefix"]/a[last()-1]/text()').extract()[0]
        for i in range(1,int(page)):
            page_url = response.url + "p" + str(i)
            #print("开始到列表页")
            yield scrapy.Request(url=page_url,callback=self.parse_page,meta=response.meta)



    def parse_page(self, response):
        item = response.meta["data"]

        # 查找景点list
        scenic_spot_list = response.xpath('//div[@class="searchresult_product basefix jj_pr"]')
        # 遍历景点list
        for scenic_spot in scenic_spot_list:
            # 景点名称
            scenic_spot_name = scenic_spot.xpath(
                './div[@class="product_m"]/p[@class="product_scenic"]/span[@class="tag_a"]/text()').extract()[0]
            item["scenic_spot_name"] = str(scenic_spot_name)
            #print(scenic_spot_name)

            # 景点评分
            scenic_spot_stars = scenic_spot.xpath(
                './div[@class="product_m"]/p[@class="product_scenic"]/span[@class="tag_b"]/text()').extract()[0]
            item["scenic_spot_stars"] = str(scenic_spot_stars)

            # hotel_name = scrapy.Field()  # 入住酒店
            hotel_name = scenic_spot.xpath(
                './div[@class="product_m"]/p[@class="product_htl"]/span[@class="tag_a"]/text()').extract()[0]
            item["hotel_name"] = str(hotel_name)

            # hotel_stars = scrapy.Field()  # 酒店评分
            hotel_stars = scenic_spot.xpath(
                './div[@class="product_m"]/p[@class="product_htl"]/span[@class="tag_b"]/i/@title').extract()[0]
            item["hotel_stars"] = str(hotel_stars)

            # days = scrapy.Field()  # 起住天数
            days = scenic_spot.xpath(
                './div[@class="product_m"]/p[@class="product_time"]/span[@class="tag_a"]/text()').extract()[0]
            item["days"] = str(days)

            # intor = scrapy.Field()  # 5, 简单介绍:
            intor= scenic_spot.xpath('./div[@class="product_m"]/h2/a/text()').extract()[0]
            item["intor"] = str(intor)


            #scenic_spot_url 景点详情url
            scenic_spot_url = scenic_spot.xpath('./div[@class="product_m"]/h2/a/@href').extract()[0]
            item["scenic_spot_url"] = str(scenic_spot_url)


            # price = scrapy.Field()  # 6, 套餐起价:
            price = scenic_spot.xpath('//p[@class="pr_price"]/strong/text()').extract()[0]
            item["price"] = "¥" + str(price)


            yield item




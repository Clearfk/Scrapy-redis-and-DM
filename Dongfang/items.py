# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongfangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    good_title = scrapy.Field()#名字
    good_price = scrapy.Field()#价格
    good_place = scrapy.Field()#产地
    good_score = scrapy.Field()#评分
    good_id = scrapy.Field()#商品id
    good_url = scrapy.Field()#商品链接
    good_com = scrapy.Field()#商品评论数

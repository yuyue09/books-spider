# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    name = scrapy.Field() #书名
    author=scrapy.Field() #作者
    message=scrapy.Field()#出版信息
    rateNums=scrapy.Field() #评价人数
    score=scrapy.Field() #评分
    summary=scrapy.Field() #简介
    book_id=scrapy.Field()#书籍的标识
    tag=scrapy.Field()#书籍标签

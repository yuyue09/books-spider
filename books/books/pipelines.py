# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import pymysql

def dbConnection():
    conn=pymysql.connect(host='localhost',port=3306,user='root',
         password='root',charset='utf8',use_unicode=False)
    return conn



class BooksPipeline(object):

    def __init__(self):
        self.file=codecs.open('items.json','w','utf-8')

    def process_item(self, item, spider):
        obj=dbConnection()
        cur=obj.cursor()
        sql='INSERT INTO douban.books(name,author,message,rateNums,score,summary,tag,book_id)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'

        try:
            cur.execute(sql,(item['name'],item['author'],item['message'],item['rateNums'],item['score'],item['summary'],item['tag'],item['book_id']))
            obj.commit()
        except Exception as e:
            print('数据存储出现错误：',e)
            obj.rollback()
        return item

    def spider_closed(self,spider):
        self.file.close()

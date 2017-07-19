# -*- coding: utf-8 -*-
import scrapy
from . .items import BooksItem
from .tags import get_urls
import re
import random

books=[]

class GoodbooksSpider(scrapy.Spider):
    name = "goodBooks"
    allowed_domains = ["book.douban.com"]
    start_urls=get_urls()#各种标签书籍的首页
   

    def parse(self, response):
        item=BooksItem()
        tag=response.xpath('//title/text()').extract()[0].split(':')
        tag=tag[-1].strip()
        for res in response.xpath('//li[@class="subject-item"]'):
            book_id=res.xpath('.//h2/a/@href').extract()[0].split('/')[-2]
            try:
                score=res.xpath('.//span[@class="rating_nums"]/text()').extract()[0]
                score=float(score)
            except:
                score=0

            try:
                rateNums=res.xpath('.//span[@class="pl"]/text()').extract()[0].strip()
                rateNums=re.sub('\n+','',rateNums)
                rateNums=re.sub(' +','',rateNums)
                rateNums=re.sub('人评价','',rateNums)
                rateNums=rateNums.strip('()')
                rateNums=int(rateNums)
            except:
                rateNums=0
                #如果该书未曾信息未曾采集，且评分不低于7，评价人数不低于100
            if book_id not in books and score>=7.0 and rateNums>=100:
                item['book_id']=book_id
                books.append(book_id)          
                try:
                    name=res.xpath('.//h2/a/@title').extract()[0]
                except Exception as e:
                    name=None
                    print('书名出现了错误',e)
                item['name']=name

            
                pubs=res.xpath('.//div[@class="pub"]/text()').extract()[0].strip()
                pubs=re.sub('\n+','',pubs)
                pubs=re.sub(' +','',pubs)
                item['message']=pubs
                try:
                    item['author']=pubs.split('/')[0]
                except:
                    item['author']=pubs.split('/')[0]

            
                item['rateNums']=rateNums

                item['score']=score

                try:
                    summary=res.xpath('.//p/text()').extract()[0].strip()
                    summary=re.sub('\n+','',summary)
                    summary=re.sub(' +','',summary)
                except:
                    summary=None
                item['summary']=summary

                item['tag']=tag

                yield item
            else:
                pass

        page=response.xpath('//span[@class="thispage"]/text()').extract()[0]
        page=int(page)#当前页数
        #因为50页后没有数据，所以不必抓取
        if response.xpath('//span[@class="next"]/a/@href').extract()[0] and page<50:
            nextUrl=response.xpath('//span[@class="next"]/a/@href').extract()[0]
            nextUrl='https://book.douban.com/'+nextUrl
            yield scrapy.Request(nextUrl,callback=self.parse)

        return item
       

        

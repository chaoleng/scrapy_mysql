# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    #默认解析方法
    def parse(self, response):
        #循环电影条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em//text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='item']//div[@class='hd']//a//span[1]//text()").extract_first()
            content = i_item.xpath(".//div[@class='item']//div[@class='bd']//p[1]//text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//div[@class='item']//div[@class='star']//span[@class='rating_num']//text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='item']//div[@class='star']//span[4]//text()").extract_first()
            douban_item['describ'] = i_item.xpath(".//div[@class='item']//p[@class='quote']//span//text()").extract_first()
            #将数据yield到pipeline里面，进行数据的清洗和存储
            yield douban_item
        #解析下一页
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)

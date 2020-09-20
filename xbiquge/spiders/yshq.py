# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem

class SancunSpider(scrapy.Spider):
    name = 'yshq'
    allowed_domains = ['www.778buy.com']
    #start_urls = ['http://www.xbiquge.la/10/10489/']

    def start_requests(self):
        start_urls = ['http://www.778buy.com/659_659168/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #dl = response.css('#list dl dd')     #提取章节链接相关信息
        dl = response.css('#defaulthtml4 > table > tr')
        dl_1 = dl.css('td a::attr(href)')
        for dd in dl_1:
            #self.url_c = "http://www.xbiquge.la" + dd.css('a::attr(href)').extract()[0]   #组合形成小说的各章节链接
            self.url_c = dd.extract()
            #print(self.url_c)
            #yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)
            yield scrapy.Request(self.url_c, callback=self.parse_c)    #以生成器模式（yield）调用parse_c方法获得各章节链接、上一页链接、下一页链接和章节内容信息。
            #print(self.url_c)
    def parse_c(self, response):
        item = XbiqugeItem()
        item['url'] = response.url
        item['preview_page'] = "http://www.778buy.com/659_659168/" + response.css('#bgdiv > table.border_l_r > tbody > tr:nth-child(2) > td > a:nth-child(1)::attr(href)').extract()[0]
        item['next_page'] = "http://www.778buy.com/659_659168/"+ response.css('#bgdiv > table.border_l_r > tbody > tr:nth-child(2) > td > a:nth-child(3)::attr(href)').extract()[0]
        title = response.css('#bgdiv > table.border_l_r > tbody > tr:nth-child(1) > td > div > h1::text').extract()[0]
        contents = response.css('div #content::text').extract()
        text=''
        for content in contents:
            text = text + content
        #print(text)
        item['content'] = title + "\n" + text.replace('\15', '\n')     #各章节标题和内容组合成content数据，\15是^M的八进制表示，需要替换为换行符。
        yield item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。


# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem
from xbiquge.pipelines import XbiqugePipeline

class SancunSpider(scrapy.Spider):
    name = 'tsxsy_bbsgx'
    allowed_domains = ['www.bbsgx.com']
    #start_urls = ['http://www.xbiquge.la/10/10489/']
    url_ori= "http://www.bbsgx.com"
    url_firstchapter = "http://www.bbsgx.com/book_211549/65039517.html"
    name_txt = "./novels/贴身小神医bbsgx"

    pipeline=XbiqugePipeline()
    pipeline.createtable(name)
    item = XbiqugeItem()
    item['name'] = name
    item['url_firstchapter'] = url_firstchapter
    item['name_txt'] = name_txt

    def start_requests(self):
        start_urls = ['http://www.bbsgx.com/book_211549/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dl = response.css('#list dl dd')     #提取章节链接相关信息
        for dd in dl:
            self.url_c = self.url_ori + '/book_211549/' + dd.css('a::attr(href)').extract()[0]   #组合形成小说的各章节链接
            #print(self.url_c)
            #yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)
            yield scrapy.Request(self.url_c, callback=self.parse_c)    #以生成器模式（yield）调用parse_c方法获得各章节链接、上一页链接、下一页链接和章节内容信息。
            #print(self.url_c)
    def parse_c(self, response):
        #item = XbiqugeItem()
        #item['name'] = self.name
        #item['url_firstchapter'] = self.url_firstchapter
        #item['name_txt'] = self.name_txt
        self.item['url'] = response.url
        self.item['preview_page'] = self.url_ori + response.css('#wrapper > div.content_read > div > div.bookname > div.bottem1 > a:nth-child(2)::attr(href)').extract()[0]
        self.item['next_page'] = self.url_ori + response.css('#wrapper > div.content_read > div > div.bookname > div.bottem1 > a:nth-child(4)::attr(href)').extract()[0]
        title = response.css('#wrapper > div.content_read > div > div.bookname > h1::text').extract()[0]
        contents = response.css('#content::text').extract()
        text=''
        for content in contents:
            text = text + content
        #print(text)
        self.item['content'] = title + "\n" + text.replace('\15', '\n')     #各章节标题和内容组合成content数据，\15是^M的八进制表示，需要替换为换行符。
        yield self.item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。

        if self.item['url'][33:41] == self.item['next_page'][33:41]:
            self.url_c = self.item['next_page']
            yield scrapy.Request(self.url_c, callback=self.parse_c)
        

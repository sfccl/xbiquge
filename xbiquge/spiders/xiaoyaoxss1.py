# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem

class SancunSpider(scrapy.Spider):
    name = 'xiaoyaoxss1'
    allowed_domains = ['www.booktxt.net']
    #start_urls = ['http://www.xbiquge.la/10/10489/']

    def start_requests(self):
        start_urls = ['https://www.booktxt.net/4_4579/2161376.html','https://www.booktxt.net/4_4579/2239769.html',
'https://www.booktxt.net/4_4579/3000148.html','https://www.booktxt.net/4_4579/3181759.html']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_c)

    def parse_c(self, response):
        item = XbiqugeItem()
        item['url'] = response.url
        item['preview_page'] = "https://www.booktxt.net/4_4579/" + response.css('#wrapper div div div.bottem2 a::attr(href)').extract()[1]
        item['next_page'] = "https://www.booktxt.net/4_4579/" + response.css('#wrapper div div div.bottem2 a::attr(href)').extract()[3]
        title = response.css('#wrapper div div div.bookname h1::text').extract()[0]
        contents = response.css('#wrapper div div #content::text').extract()
        text=''
        for content in contents:
            text = text + content
        item['content'] = title + "\n" + text.replace('\15', '\n')     #各章节标题和内容组合成content数据，\15是^M的八进制表示，需要替换为换行符。
        yield item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。


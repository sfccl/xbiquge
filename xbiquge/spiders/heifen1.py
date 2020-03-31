# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem
class SancunSpider(scrapy.Spider):
    name = 'heifen1'
    allowed_domains = ['www.xbiquge.la']
    #start_urls = ['http://www.xbiquge.la/10/10489/']

    def start_requests(self):
        start_urls = ['http://www.xbiquge.la/43/43474/19425972.html']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = XbiqugeItem()
        item['url'] = response.url
        item['preview_page'] = "http://www.xbiquge.la" + response.css('div .bottem1 a::attr(href)').extract()[1]
        item['next_page'] = "http://www.xbiquge.la" + response.css('div .bottem1 a::attr(href)').extract()[3]
        title = response.css('.con_top::text').extract()[4]
        contents=response.css('#content::text').extract()
        text=''
        for content in contents:
            text = text + content
        #print(text)
        text = EmojiParser.removeAllEmojis(text)
        item['content'] = title + "\n" + text.replace('\15', '\n')     #各章节标题和内容组合成content数据，\15是^M的八进制表>示，需要替换为换行符。
        yield item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。


'''
    def parse(self, response):
        dl = response.css('#list dl dd')     #提取章节链接相关信息
        for dd in dl:
            self.url_c = "http://www.xbiquge.la" + dd.css('a::attr(href)').extract()[0]   #组合形成小说的各章节链接
            #print(self.url_c)
            #yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)
            yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)    #以生成器模式（yield）调用parse_c方法获得各章节链接、上一页链接、下一页链接和章节内容信息。
            #print(self.url_c)



    def parse(self, response):
        item = XbiqugeItem()
        item['url'] = response.url
        item['preview_page'] = "http://www.xbiquge.la" + response.css('div .bottem1 a::attr(href)').extract()[1]
        item['next_page'] = "http://www.xbiquge.la" + response.css('div .bottem1 a::attr(href)').extract()[3]
        title = response.css('.con_top::text').extract()[4]
     =     contentsresponse.css('#content::text').extract()
        text=''
        for content in contents:
            text = text + content
        #print(text)
        item['content'] = title + "\n" + text.replace('\15', '\n').replace(u'\xf0\x9f\x8d\xbb\xe2\x80', u'')     #各章节标题和内容组合成content数据，\15是^M的八进制表示，需要替换为换行符。
        yield item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。
'''

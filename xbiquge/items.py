# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XbiqugeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url_firstchapter = scrapy.Field()
    name_txt = scrapy.Field()
    url = scrapy.Field()
    preview_page = scrapy.Field()
    next_page = scrapy.Field()
    content = scrapy.Field()

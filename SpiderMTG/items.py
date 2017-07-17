# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Auction(scrapy.Item):
    title = scrapy.Field()
    card = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    expansion = scrapy.Field()
    language = scrapy.Field()
    condition = scrapy.Field()
    extra = scrapy.Field()
    href = scrapy.Field()
    bids = scrapy.Field()
    time_left = scrapy.Field()

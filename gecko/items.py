# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BrandItem(scrapy.Item):
    brand = scrapy.Field()
    brand_link = scrapy.Field()
    created_time = scrapy.Field()
    #brand_name = scrapy.Field()
    #description = scrapy.Field()
    #product_url = scrapy.Field()



class ProductItem(scrapy.Item):
    brand_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    weight = scrapy.Field()
    price = scrapy.Field()
    short_description = scrapy.Field()
    long_description = scrapy.Field()
    usage = scrapy.Field()
    composition = scrapy.Field()
    ingredient = scrapy.Field()
    conservation = scrapy.Field()
    nutritionnelles = scrapy.Field()
    promotion = scrapy.Field()
    created_time = scrapy.Field()

class LastnameItem(scrapy.Item):
    lastname = scrapy.Field()
    brand_link = scrapy.Field()
    created_time = scrapy.Field()


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeruaItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    photo_links = scrapy.Field()
    country = scrapy.Field()
    weight = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    depth = scrapy.Field()
    length = scrapy.Field()


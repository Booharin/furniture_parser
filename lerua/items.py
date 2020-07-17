# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(value):
    if 'w_1200' in value:
        return value


def clean_price(value):
    return int(value.replace(' ', ''))


def clean_parameter(value):
    return value.replace(' ', '')\
        .replace('\n', '')


def float_parameter(value):
    return float(clean_parameter(value))


class LeruaItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())

    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=MapCompose(clean_price),
        output_processor=TakeFirst()
    )
    photo_links = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    parameters_dict = scrapy.Field(input_processop=MapCompose)

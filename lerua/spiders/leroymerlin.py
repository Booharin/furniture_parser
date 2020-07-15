import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lerua.items import LeruaItem
import re

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        furniture_links = response.css('a.black-link')
        for link in furniture_links:
            yield response.follow(link, callback=self.parse_furniture)

    def parse_furniture(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('link', response.url)
        loader.add_css('price', 'span[slot=price]::text')
        loader.add_css('photo_links', 'uc-pdp-media-carousel[slot=media-content] img::attr(src)')

        parameters = response.css('div[class=def-list__group]')
        parameters_dict = {}
        for parameter in parameters:
            key = parameter.css('dt[class=def-list__term]::text')\
                .extract_first()\
                .replace('\n', '')
            value = parameter.css('dd[class=def-list__definition]::text')\
                .extract_first()\
                .replace(' ', '')\
                .replace('\n', '')

            if self.hasNumbers(value):
                try:
                    value = float(value)
                except Exception as e:
                    print(e)

            parameters_dict[key] = value

        loader.add_value('parameters_dict', parameters_dict)
        yield loader.load_item()

    def hasNumbers(self, inputString):
        return bool(re.search(r'\d', inputString))
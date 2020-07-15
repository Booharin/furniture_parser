import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lerua.items import LeruaItem

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
        loader.add_xpath('weight', "//div[dt[text()='Вес, кг']]//dd/text()")
        loader.add_xpath('country', "//div[dt[text()='Страна производства']]//dd/text()")
        loader.add_xpath('width', "//div[dt[text()='Общая ширина (см)']]//dd/text()")
        loader.add_xpath('height', "//div[dt[text()='Общая высота (см)']]//dd/text()")
        loader.add_xpath('depth', "//div[dt[text()='Глубина (см)']]//dd/text()")
        loader.add_xpath('length', "//div[dt[text()='Длина (см)']]//dd/text()")

        yield loader.load_item()
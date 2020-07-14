import scrapy
from scrapy.http import HtmlResponse
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
        link = response.url
        title = response.css('h1::text').extract_first()
        price = int(response.css('span[slot=price]::text').extract_first())
        photo_links = list(
            filter(
                lambda s: 'w_1200' in s,
                response.css('uc-pdp-media-carousel[slot=media-content] img::attr(src)').extract()
            )
        )
        weight = float(
            response.xpath("//div[dt[text()='Вес, кг']]//dd/text()")
            .extract_first().replace(' ', '')
            .replace('\n', '')
        )
        country = response.xpath("//div[dt[text()='Страна производства']]//dd/text()")\
            .extract_first()\
            .replace(' ', '')\
            .replace('\n', '')
        width = float(
            response.xpath("//div[dt[text()='Общая ширина (см)']]//dd/text()")
                .extract_first().replace(' ', '')
                .replace('\n', '')
        )
        height = float(
            response.xpath("//div[dt[text()='Общая высота (см)']]//dd/text()")
                .extract_first().replace(' ', '')
                .replace('\n', '')
        )
        depth = float(
            response.xpath("//div[dt[text()='Глубина (см)']]//dd/text()")
                .extract_first().replace(' ', '')
                .replace('\n', '')
        )
        length = float(
            response.xpath("//div[dt[text()='Длина (см)']]//dd/text()")
                .extract_first().replace(' ', '')
                .replace('\n', '')
        )

        yield LeruaItem(title=title,
                        link=link,
                        price=price,
                        weight=weight,
                        country=country,
                        width=width,
                        height=height,
                        depth=depth,
                        length=length,
                        photo_links=photo_links)
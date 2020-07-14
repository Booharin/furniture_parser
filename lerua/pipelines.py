from scrapy.pipelines.images import ImagesPipeline
import scrapy

class DataBasePipeline:
    def process_item(self, item, spider):
        print(1)
        return item

class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo_links']:
            for img_link in item['photo_links']:
                try:
                    yield scrapy.Request(img_link)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print(1)


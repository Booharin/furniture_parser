from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy


class DataBasePipeline:
    def __init__(self):
        self.mongo_client = MongoClient("mongodb://admin:12345@18.197.155.243/my_db")
        self.photos = self.mongo_client.my_db.photos

    def process_item(self, item, spider):
        self.photos.replace_one(item, item, upsert=True)
        return item

    def __del__(self):
        self.mongo_client.close()


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo_links']:
            for img_link in item['photo_links']:
                try:
                    yield scrapy.Request(img_link, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        name = request.url.split('/')[-1]
        return f"/{item['title']}/{name}.jpg"


    def item_completed(self, results, item, info):
        if results:
            item['photo_links'] = [itm[1] for itm in results if itm[0]]
        return item


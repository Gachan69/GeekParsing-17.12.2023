# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class GbParsePipeline:
    def process_item(self, item, spider):
        return item


class GbParseMongoPipeline:

    def __init__(self):
        client = pymongo.MongoClient('mongodb+srv://Daniel:-p@atlascluster.afucu8k.mongodb.net/')
        self.db = client['geek_parsing']

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(dict(item))
        return item


class ImageDownloadPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get('photo', []):
            yield Request(url)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results]
        return item

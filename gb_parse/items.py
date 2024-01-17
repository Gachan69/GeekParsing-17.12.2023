# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Gba4fragItem(scrapy.Item):
    url = scrapy.Field()
    photo = scrapy.Field()
    item = scrapy.Field()
    product = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    stats = scrapy.Field()

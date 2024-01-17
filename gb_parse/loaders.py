from scrapy.loader import ItemLoader
from scrapy import Selector
from .items import Gba4fragItem
from itemloaders.processors import TakeFirst, MapCompose
from itemloaders.processors import Compose


# def get_first(items: list):
#     for itm in items:
#         if itm:
#             return itm

def get_stats(item):
    selector = Selector(text=item)
    data = {
        'title': selector.xpath("//th[contains(@scope,'row')]/text()").extract_first(),
        'value': selector.xpath("//td/text()").extract_first()}
    return data
# MapCompose


# def get_description(item):
#     selector = Selector(text=item)
#     data = {
#         'title': selector.xpath("//th[@scope='row']"),
#         'value': selector.xpath("//div[@id='tab-2']//td")}

class A4fragLoader(ItemLoader):
    default_item_class = Gba4fragItem
    url_out = TakeFirst()
    photo_out = TakeFirst()
    product_out = TakeFirst()
    item_out = Compose(lambda v: v[1], str.strip)
    price_out = TakeFirst()
    stats_in = MapCompose(get_stats)


    # если в выгрузке много ключей div и тд
    # MapCompose
    # description_in = MapCompose(get_description)

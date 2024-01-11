import pymongo
import scrapy


class A4fragSpider(scrapy.Spider):
    name = "4frag"
    allowed_domains = ["4frag.ru"]
    start_urls = ["https://4frag.ru/"]

    _css_selectors = {
        'devices': '.dropdown-submenu .parent',
        'pagination': '.col-pager a',
        'item-link': '.item-link'
    }
    data_query = {
        'item': lambda resp: resp.css('.breadcrumb-item-box span ::text').extract()[1],
        'product': lambda resp:  resp.css('.row h1::text').extract_first(),
        'price': lambda resp: resp.css('.item-price::text').extract_first(),
        'description': lambda resp:  (resp.css('[style="text-align:justify"]::text').extract()
                                      or resp.css('[style="text-align: justify;"]::text').extract()),
        'stats': lambda resp: resp.css('tbody').extract()

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get('href')
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        # devices = response.css(self._css_selectors['devices'])
        yield from self._get_follow(response,
                                    self._css_selectors['devices'],
                                    self.device_parse, hello='moto')
        # for device_a in devices:
        #     link = device_a.attrib.get('href')
        #     yield response.follow(link, callback=self.device_parse, cb_kwargs={'hello': 'Moto'})

    def device_parse(self, response, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors['pagination'],
                                    self.device_parse)
        # for pag_a in response.css(self._css_selectors['pagination']):
        #     link = pag_a.attrib.get('href')
        #     yield response.follow(link,callback=self.device_parse)

        yield from self._get_follow(response,
                                    self._css_selectors['item-link'],
                                    self.item_link_parse)
        # for item_link_a in response.css(self._css_selectors['item-link']):
        #      link = item_link_a.atrib.get('href')
        #      yield response.follow(link, callback=self.item_link_parse)

    def item_link_parse(self, response):
        data = {}
        for key, selector in self.data_query.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        yield data
        # product = response.css('.row h1::text').extract_first()
        # price = response.css('.item-price::text').extract_first()
        # description = (response.css('[style="text-align:justify"]::text').extract()
        #                or response.css('[style="text-align: justify;"]::text').extract())
        # stats = response.css('tbody').extract()
        # tip = response.css('.breadcrumb-item-box span ::text').extract()[1]


        print(1)

import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.a4frag import A4fragSpider
from gb_parse.spiders.zillow import ZillowSpider

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
    crawler_settings = Settings()
    crawler_settings.setmodule('gb_parse.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(ZillowSpider)
    crawler_proc.start()
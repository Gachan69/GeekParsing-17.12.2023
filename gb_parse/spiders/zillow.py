import scrapy
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ZillowSpider(scrapy.Spider):
    name = "zillow"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/homes/New-York,-NY_rb/"]
    page_xpath = {
        'pagination': '//nav[@aria-label="Pagination"]/ul/li/a/@href',
        'ads': '//div [@id="grid-search-results"]//a/@href',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = webdriver.Chrome()

    def _get_follow_xpath(self, response, select_str, callback, **kwargs):
        for link in response.xpath(select_str):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response):
        yield from  self._get_follow_xpath(response,
                                           self.page_xpath['pagination'],
                                           self.parse)
        yield from self._get_follow_xpath(response,
                                          self.page_xpath['ads'],
                                          self.ads_parse)

    def ads_parse(self, response):
        self.browser.get(response.url)
        print(1)
        button = self.browser.find_element(By.XPATH, '//button[@type="button"]')
        media_wall = self.browser.find_element(By.XPATH, '//div[@data-testid="hollywood-photo-carousel"]/div')
        len_photos = media_wall.find_element(By.XPATH,'//button/picture')
        # while True:
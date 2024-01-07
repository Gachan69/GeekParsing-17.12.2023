from pathlib import Path
import bs4
import requests
import pymongo


url = 'https://small.kz/ru/almaty/catalog-goods?page=1'
file_path = Path(__file__).parent.joinpath('small.html')
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')

print(1)


class SmallParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client['geek_parsing']
        self.collection = self.db['small_products']

    def _get_response(self, url):
        return requests.get(url)
    #     TODO: обработка ошибки

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': 'goods'})
        for prod_p in catalog.find_all('div', recursive=False):
            product_data = self._parse(prod_p)
            self._save(product_data)

    def get_template(self):

        return {
            'title': lambda a: a.find('div', attrs={'class': "goodInfo"}).text.replace('  ', ''),
            'activeprice': lambda a: a.find('div', attrs={'class': "activePrice"}).text.strip(' \n\t'),
            'oldprice': lambda a: a.find('div', attrs={'class': "oldPrice"}).text.strip(' \n\t'),
            'promo_name': lambda a: a.find('div', attrs={'class': "salePercent"}).text.strip(' \n\t'),
        }


    def _parse(self, product_p) -> dict:
        data = {}
        for key, funk in self.get_template().items():
            try:
                data[key] = funk(product_p)
            except AttributeError:
                pass
        return data


    def _save(self, data: dict):
        self.collection.insert_one(data)
        print(1)


def get_save_path(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == '__main__':
    url = 'https://small.kz/ru/almaty/catalog-goods'

    save_path = get_save_path('small_product')
    # db_client = pymongo.MongoClient('mongodb://login:password@localhost:27017/db_name')
    db_client = pymongo.MongoClient('mongodb+srv://Daniel:BAM-7351@atlascluster.afucu8k.mongodb.net/')

    parser = SmallParse(url, db_client)
    parser.run()
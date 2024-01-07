import pymongo

db_client = pymongo.MongoClient('mongodb+srv://Daniel:BAM-7351@atlascluster.afucu8k.mongodb.net/')
db = db_client['geek_parsing']
collection = db['small_products']

template_data = {'some_name': 'hello', '2': 2222}
collection.insert_one(template_data)
for product in collection.find({'title': {'$regex': '[Х|х]лопья'},'promo_name': '20%'}):
    print(product)
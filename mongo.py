'''
# https://github.com/mongodb-developer/python-mongodb
# https://www.mongodb.com/languages/python
'''
import pymongo
import pandas as pd
from dateutil import parser

uri = "uri here"

def get_database():
    client = pymongo.MongoClient(uri)
    db = client.test
    return db['user_shopping_list']

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    collection_name = dbname['user_1_items']
    collection_name.insert_many([item_1,item_2])
    collection_name.insert_one(item_3)

def test_query():
    dbname = get_database()
    collection_name = dbname['user_1_items']
    # item_details = collection_name.find()
    # for item in item_details:
    #     print(item['_id'],item['category'])

    item_details = collection_name.find({"category" : "food"})
    items_df = pd.DataFrame(item_details)
    print(items_df[['item_name','category','order_date']])

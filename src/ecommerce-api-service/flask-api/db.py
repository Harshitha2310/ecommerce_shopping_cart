# importing module
from bson.json_util import dumps
from pymongo import MongoClient
import pymongo
from s3 import s3_delete


# creation of MongoClient
client=MongoClient()

# Connect with the portnumber and host
client = pymongo.MongoClient("mongodb+srv://test:Track97@cluster1.lx4ei2l.mongodb.net/?retryWrites=true&w=majority")

mydb = client.test
products = mydb["product"]
orders = mydb["order"]
reviews = mydb["review"]

def insert_data(collection, data_list)->bool:
    mycol = mydb[collection]
    for data in data_list:
        mycol.insert_one(data)
    return True


# product = [{ "product_id": "3", "type": "camera" , "product_name": "SONY", "price": "1000", "s3_path": "dummy"},
# { "product_id": "4", "type": "camera" , "product_name": "SONY", "price": "1000", "s3_path": "dummy"}]
# insert_data("products", product)

# order = [{ "order_id": "001",  "product_id": "1", "emailid": "test@gmail.com", "datetime": "2022-09-08 00:00:00", 
# "quantity": "10", "delivery_date": "2022-09-12", "status":"ordered"}]
# insert_data("orders", order)
 
# review = [{ "product_id": "1", "datetime": "2022-09-08 00:00:00", 
# "emailid": "test@gmail.com", "rating": "3", "comment": "Nice Camera!!!"}]
# insert_data("reviews", review)


def list_products():
    prods = products.find()
    list_cur = list(prods)
    json_data = dumps(list_cur)
    return json_data 

def list_orders():
    ordered_items = orders.find()
    list_cur = list(ordered_items)
    json_data = dumps(list_cur)
    return json_data 

def list_reviews_for_items():
    re_view = reviews.find()
    list_cur = list(re_view)
    json_data = dumps(list_cur)
    return json_data 

def delete_product(query):
    products.delete_one(query)
    s3_delete(query["product_id"])
    return "success"

def delete_order(query):
    orders.delete_one(query)
    return "success"

def delete_review(query):
    reviews.delete_one(query)
    return "success"



# Review
# product_id
# emailid
# rating[1-4]
# comments
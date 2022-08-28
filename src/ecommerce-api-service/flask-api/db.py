# importing module
from pymongo import MongoClient
import pymongo
# creation of MongoClient
client=MongoClient()

# Connect with the portnumber and host
client = pymongo.MongoClient("mongodb+srv://test:Track97@cluster1.lx4ei2l.mongodb.net/?retryWrites=true&w=majority")

mydb = client.test

def insert_data(collection, data_list)->bool:
    mycol = mydb[collection]
    for data in data_list:
        mycol.insert_one(data)
    return True


product = [{ "product_id": "3", "type": "camera" , "product_name": "SONY", "price": "1000"},
{ "product_id": "4", "type": "camera" , "product_name": "SONY", "price": "1000"}]
insert_data("products", product)

order = [{ "order_id": "001",  "product_id": "1", "emailid": "test@gmail.com", "datetime": "2022-09-08 00:00:00", 
"quantity": "10", "delivery_date": "2022-09-12", "status":"ordered"}]

insert_data("orders", order)
 
review = [{ "product_id": "1", "datetime": "2022-09-08 00:00:00", 
"emailid": "test@gmail.com", "rating": "3", "comment": "Nice Camera!!!"}]

insert_data("reviews", review)


# Review
# product_id
# emailid
# rating[1-4]
# comments
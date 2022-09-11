from flask import Flask, request
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from db import insert_data, list_products, list_orders, list_reviews_for_items, delete_product, delete_order, delete_review
from s3 import s3_upload, s3_delete
import jsonify


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# xray_recorder.configure(service='ecommerce-api-service')
# XRayMiddleware(app, xray_recorder)

@app.route('/')
def healthcheck():
    return 'Up and Running'
 
@app.route('/add_product', methods=['POST'])
def add_product():
    content = request.json 
    insert_data('product', content['product'])
    return "success"

@app.route('/order_product', methods=['POST'])
def order_product():
    content = request.json 
    insert_data('order', content['order'])
    return "success"

@app.route('/review', methods=['POST'])
def customer_review():
    content = request.json 
    insert_data('review', content['review'])
    return "success"

@app.route('/list_products', methods=['GET'])
def list_prods():
    products = list_products()
    return products

@app.route('/list_orders', methods=['GET'])
def list_order_details():
    orders= list_orders()
    return orders

@app.route('/list_reviews', methods=['GET'])
def list_reviews_of_product():
    reviews = list_reviews_for_items()
    return reviews

@app.route('/delete_product', methods=['POST'])
def delete_prod():
    content = request.json 
    return delete_product(content)

@app.route('/delete_order', methods=['POST'])
def delete_ordered_item():
    content = request.json 
    return delete_order(content)

@app.route('/delete_review', methods=['POST'])
def delete_reviewed_item():
    content = request.json 
    return delete_review(content)

@app.route('/upload_prod_img', methods=['POST'])
def upload_product_image():
    file = request.files["file"]
    return s3_upload(file)

if __name__ == '__main__':
    app.run(debug=True)
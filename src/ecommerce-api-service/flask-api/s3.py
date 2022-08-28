import boto3
import io
s3 = boto3.client("s3")
BUCKET_NAME = "poc-ecommerce-2022"

def s3_upload(file_binary, s3_path)->bool:
    file_as_binary = io.BytesIO(file_binary)
    s3.upload_fileobj(file_as_binary,BUCKET_NAME,s3_path)
    return True
def s3_delete(s3_path)->bool:
    s3.delete_object(Bucket = BUCKET_NAME, Key=s3_path)
    return True

file_binary = open("D:/ecommerce-website/git/ecommerce_shopping_cart/src/ecommerce-api-service/flask-api/camera.jpg", "rb").read()
s3_upload(file_binary, "products/1")

# s3_delete("products/1")
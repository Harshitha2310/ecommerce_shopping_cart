import boto3
import io
s3 = boto3.client("s3")
BUCKET_NAME = "poc-ecommerce-2022"
s3_path = "products"

def s3_upload(file)->bool:
    # file_as_binary = io.BytesIO(file_binary)
    print("laptop",file.filename)
    filename = file.filename
    filesplit = filename.split(".")
    s3.upload_fileobj(file,BUCKET_NAME,s3_path+"/"+filesplit[0])
    return "success"

def s3_delete(pid)->bool:
    s3.delete_object(Bucket = BUCKET_NAME, Key=s3_path+"/"+pid)
    return "success"

# file_binary = open("D:/ecommerce-website/git/ecommerce_shopping_cart/src/ecommerce-api-service/flask-api/camera.jpg", "rb").read()
# s3_upload(file_binary, "products/1")


# s3_delete("products/1")
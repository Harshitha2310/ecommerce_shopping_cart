from flask import Flask
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)

xray_recorder.configure(service='ecommerce-api-service')
XRayMiddleware(app, xray_recorder)

@app.route('/')
def healthcheck():
    return 'Up and Running'
 

if __name__ == '__main__':
    app.run()
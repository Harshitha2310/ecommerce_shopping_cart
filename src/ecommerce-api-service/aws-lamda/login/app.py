import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json

# Define user pool details
USER_POOL_ID = 'ap-south-1_HKVguryST'
CLIENT_ID = '18ld5u2r52qm1qkrvc0145jubh'
CLIENT_SECRET = '172m8riipfkcie6hgp4668tdmnk63g1plqg9dvq9dk0e8ildigq0'

# Create secret hash
def get_shash(username):
    # convert str to bytes
    key = bytes(CLIENT_SECRET, 'latin-1')  
    msg = bytes(username + CLIENT_ID, 'latin-1')  
    digest = hmac.new(key, msg, hashlib.sha256).digest()   
    return base64.b64encode(digest).decode()

# Initiate authentication
def initiate_auth(client, username, password):
    secret_hash = get_shash(username)
    
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            }
        )
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None

def lambda_handler(event, context):
 
 

    # Load the Cognito IDP client
    client = boto3.client('cognito-idp')
    
    email = event["email"]
    password = event["password"]
    
    resp, msg = initiate_auth(client, email, password)
   
    if msg != None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': msg, 
                'error': True, 
                'success': False, 
                'data': None                
            })
        }

    if resp.get("AuthenticationResult"):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': "success", 
                'error': False, 
                'success': True, 
                'data': {
                    'id_token': resp["AuthenticationResult"]["IdToken"],
                    'refresh_token': resp["AuthenticationResult"]["RefreshToken"],
                    'access_token': resp["AuthenticationResult"]["AccessToken"],
                    'expires_in': resp["AuthenticationResult"]["ExpiresIn"],
                    'token_type': resp["AuthenticationResult"]["TokenType"] 
                }
            })
        }
    else: #this code block is relevant only when MFA is enabled
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': True, 
                'success': False, 
                'data': None, 
                'message': None                
            })
        }
import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

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
    
def lambda_handler(event, context):
    # Load cognito-idp client
    client = boto3.client('cognito-idp')
    
     
    
    try:
        email = event['email']
        
        response = client.forgot_password(
            ClientId=CLIENT_ID,
            SecretHash=get_shash(email),
            Username=email
        )
    except client.exceptions.UserNotFoundException:
        return {
            'statusCode': 409,
            'body': json.dumps({
                'error': True, 
                'success': False,
                'message': "Username doesnt exists",
                'data': None
            })
        }
    except client.exceptions.InvalidParameterException:
        return {
            'statusCode': 409,
            'body': json.dumps({
                'error': True, 
                'success': False,
                'message': f"User <{email}> is not confirmed yet",
                'data': None
            })
        }
    except client.exceptions.CodeMismatchException:
        return {
            'statusCode': 409,
            'body': json.dumps({
                'error': True, 
                'success': False, 
                'message': "Invalid Verification code",
                'data': None
            })
        }
    except client.exceptions.NotAuthorizedException:
        return {
            'statusCode': 401,
            'body': json.dumps({
                'error': True, 
                'success': False,
                'message': "User is already confirmed",
                'data': None
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': True, 
                'success': False,
                'message': f"Uknown error {e.__str__()} ",
                'data': None
            })
        }
     
    return {
        'statusCode': 200,
        'body': json.dumps({
            'error': False, 
            'success': True, 
            'message': f"Please check your Registered email id for validation code",  
            'data': None            
        })
    }

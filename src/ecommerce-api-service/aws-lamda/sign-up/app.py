
import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64

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
    

    
    # Load the Cognito IDP client
    client = boto3.client('cognito-idp')
    
    # Sign up the new user
    try:
        email = event["email"]
        password = event['password']
        shash = get_shash(email)        
        
        response = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_shash(email),
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': "name",
                    'Value': email,
                },         
            ],
            ValidationData=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )
        
    except client.exceptions.UsernameExistsException as e:  
        return {
            'statusCode': 409,
            'body': json.dumps({
                'error': True,
                'success': False,
                'message': "This username/email already exists",
                'data': None                
            })
        }
    except client.exceptions.InvalidPasswordException as e:
        return {
            'statusCode': 401,
            'body': json.dumps({
                'error': True, 
                'success': False, 
                'message': "Password should have Caps, Special chars, Numbers",
                'data': None                
            })
        }
    except client.exceptions.UserLambdaValidationException as e:
        return {
            'statusCode': 409,
            'body': json.dumps({
                'error': True, 
                'success': False, 
                'message': "Email already exists", 
                'data': None                
            })
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': True, 
                'success': False, 
                'message': str(e),
                'data': None                
            })
        }
    return {
        'statusCode': 200,
        'body': json.dumps({
            'error': False,
            'success': True, 
            'message': 'Please confirm your signup, check Email for validation code', 
            'data': None            
        })
    }
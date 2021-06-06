from pymongo import MongoClient
from .local_settings import password, aws_access_key, aws_secret_access_key, aws_storage_bucket, aws_default_acl
from datetime import datetime
from boto3 import client
import jwt

'''
AWS CONNECTION
'''

AWS_STORAGE_BUCKET_NAME = aws_storage_bucket
AWS_DEFAULT_ACL = aws_default_acl
AWS_BASE_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
def s3Client():
    return client('s3',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_access_key)

'''
DATABASE CONNECTION
'''

def clientOpen():
    return MongoClient(f"mongodb+srv://myworld:{password}@cluster0.jzv7p.mongodb.net/myworld?retryWrites=true&w=majority")


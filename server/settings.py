from pymongo import MongoClient
from .local_settings import username, password, aws_access_key, aws_secret_access_key, aws_storage_bucket, aws_default_acl
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
    return MongoClient(f"mongodb://{username}:{password}@docdb-2021-06-22-07-54-11.cluster-cmmlvhwuwqnu.ap-south-1.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")


"""
Groups
"""

class Groups:
    def __init__(self):
        self.groups = {}

    def group_add(self, group_name, websocket_endpoint):
        if group := self.groups.get(group_name):
            group.append(websocket_endpoint)
        else:
            self.groups.update({group_name: [websocket_endpoint, ]})

    def group_discard(self, group_name, websocket_endpoint):
        if group_name in self.groups:
            self.groups[group_name].remove(websocket_endpoint)

    async def group_send(self, group_name, data):
        if group := self.groups.get(group_name):
            for i in group:
                await i.broadcast(data=data)

group = Groups()

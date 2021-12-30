from pymongo import MongoClient
from .local_settings import username, password, aws_access_key, aws_secret_access_key, aws_storage_bucket, aws_default_acl
from datetime import datetime
from boto3 import client
import jwt
from pyfcm import FCMNotification

'''
AWS CONNECTION
'''

AWS_STORAGE_BUCKET_NAME = aws_storage_bucket
AWS_DEFAULT_ACL = aws_default_acl
AWS_BASE_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
def s3Client():
    return client('s3',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_access_key)

'''
FCM
'''

push_service = FCMNotification(api_key="AAAA06zBFVA:APA91bEzn2_SeZTRipMpqImpLc3otatgjRKfxj84W-oWuLCD7R7gYx8PR4PTfSiMjs08ddGvtB2S319QXzNDapVbGJEQNIdZdRc8XA3e6tZzAtcphM7YLuYe_nZgQIy487Xr0pJTC3Vj")

def notify(token,body):
    push_service.notify_single_device(registration_id=token, message_title="Myworld", message_body=body)   
'''
DATABASE CONNECTION
'''

def clientOpen():
    #return MongoClient(f"mongodb://{username}:{password}@docdb-2021-08-31-04-49-08.cluster-cnx3ni4ekzmn.ap-south-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")
    return MongoClient(f"mongodb+srv://aiworld:i6TO1DZbtBzckOnx@mydb.xci1l.mongodb.net/mydb?retryWrites=true&w=majority")

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

from server.settings import clientOpen
from bson.json_util import loads, dumps
from datetime import datetime


class BaseUpload:

    def __init__(self):
        self.client = clientOpen()
    
    def create(self, profile_id ,title, description, duration, category, thumbnail, upload_file, timestamp):
        profile=loads(dumps(self.client.auth.profile.find_one({"_id":profile_id})))
        id=profile_id+"_"+title+"_"+str(timestamp)+"_"+category+"_"+str(duration)
        self.client.videos.upload.insert_one({
            "_id":id,
            "profile":{
                "_id":profile_id,
                "name":profile["name"],
                "channel_name":profile["channel_name"],
                "profile_picture":profile["profile_picture"]
            },
            "title":title,
            "description":description,
            "thumbnail":thumbnail,
            "duration":duration,
            "category":category,
            "upload_file":upload_file,
            "timestamp":timestamp
        })

        self.client.close()

        return id

    def get(self, id):
        res = self.client.videos.upload.find_one({
            "_id":id
        })

        self.client.close()
        return res

    def allvideos(self):
        res = loads(dumps(self.client.videos.upload.find()))
        self.client.close()
        return res

    def delete(self,video_id):
        self.client.videos.upload.delete_one({
            "_id":video_id,
        })

        self.client.close()

    def exploreImage(self,title,description,image):
        self.client.explore.images.insert_one({
            "_id":title+"_"+str(datetime.utcnow().timestamp()),
            "title":title,
            "description":description,
            "image":image,
            "timestamp":str(datetime.utcnow().timestamp())
        })
        self.client.close()
        return True

    def token(self, profile):
        return self.client.notifications.tokens.find_one({"profile":profile})["token"]



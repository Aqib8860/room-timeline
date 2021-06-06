from bson.json_util import dumps, loads
from server.settings import clientOpen
from datetime import datetime

class ViewTracker:

    def __init__(self):
        self.client = clientOpen()
    
    def total(self,video_id):
        total_duration = count = 0
        for i in loads(dumps(self.client.videos.viewtracker.find({"video_id":video_id}))):
            total_duration += i["duration"]
            count+=1

        if self.client.videos.views.find_one({"video_id":video_id}):

            self.client.videos.views.update_one({"_id":{"$regex":video_id}},{
                "$set":{
                    "total_duration":total_duration
                }})
            self.client.videos.views.update_one({"_id":{"$regex":video_id}},{
                "$set":{
                    "total_viewers":count
                }})
        else:
            self.client.videos.views.insert_one({
                    "_id":video_id+str(datetime.utcnow().timestamp()),
                    "total_duration":total_duration,
                    "total_viewers":count
            })

    def create(self, id, video_id, duration):
        if c:=self.client.videos.viewtracker.find_one({"video_id":video_id,"_id":id}):
            if c["duration"]<duration:
                self.client.videos.viewtracker.update({"video_id":video_id,"_id":id},{"$set":{"duration":duration}})
        else:
            self.client.videos.viewtracker.insert_one({"_id":id,"video_id":video_id,"duration":duration})

    def get(self,video_id):
        return loads(dumps(self.client.videos.views.find_one({"_id":{"$regex":video_id}})))

    def close(self):
        self.client.close()
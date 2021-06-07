from server.settings import clientOpen
from datetime import datetime
from bson.json_util import loads, dumps

class Like:
    def __init__(self):
        self.client = clientOpen()
    
    def create_or_delete(self,profile_id,video_id):

        if c:=self.client.videos.likes.find_one({"video_id":video_id}):

            # Delete Like

            if profile_id in c["users"]:
                self.client.videos.likes.update({"video_id":video_id},
                    {
                        "$pull":{
                            "users":profile_id
                        }
                    }
                )
                return "Like Deleted Successfully"
            
            # Add New Like To Existing Document
            self.client.videos.likes.update({"video_id":video_id},
                {
                    "$push":{
                        "users":profile_id
                    }
                }
            )
            
        else:
            # Add New Like
            self.client.videos.likes.insert_one({
                "_id":profile_id+"_"+str(datetime.utcnow().timestamp()),
                "video_id":video_id,
                "users":[profile_id]
            })

        return "Liked Successfully"

    def close(self):
        self.client.close()

class Comment:
    def __init__(self):
        self.client = clientOpen()
    
    def create(self,profile_id,video_id,comment):

        if self.client.videos.comments.find_one({"video_id":video_id}):

            # Add New Comment To Existing Document
            self.client.videos.comments.update({"video_id":video_id},
                {
                    "$push":{
                        "comments":(profile_id,comment)
                    }
                }
            )
            
        else:

            # Add New Comment
            self.client.videos.comments.insert_one({
                "_id":profile_id+"_"+str(datetime.utcnow().timestamp()),
                "video_id":video_id,
                "comments":[(profile_id,comment)]
            })

        return "Commented Successfully"

    def close(self):
        self.client.close()

class LikeCommentView:

    def __init__(self):
        self.client = clientOpen()

    def get(self, video_id):
        
        res = dict()

        res["video_id"]=video_id

        if c:=loads(dumps(self.client.videos.likes.find_one({"video_id":video_id}))):
            res["likes"]=len(c["users"])
        else:
            res["likes"]=0
        
        res["comments"]=loads(dumps(self.client.videos.comments.find_one({"video_id":video_id})))

        res["views"]=loads(dumps(self.client.videos.views.find_one({"_id":{"$regex":video_id}})))

        return res

    def close(self):

        self.client.close()

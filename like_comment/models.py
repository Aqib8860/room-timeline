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

    def user_name(self, profile_id):
        return loads(dumps(self.client.auth.profile.find_one({"_id":profile_id})))["channel_name"]

    def video_title(self, video_id):
        return loads(dumps(self.client.videos.upload.find_one({"_id":video_id})))["title"]
        
    def close(self):
        self.client.close()

class Comment:
    def __init__(self):
        self.client = clientOpen()
    
    def create(self,profile_id,video_id,comment):

        profile = loads(dumps(self.client.auth.profile.find_one({"_id":profile_id})))

        if self.client.videos.comments.find_one({"video_id":video_id}):

            # Add New Comment To Existing Document
            self.client.videos.comments.update({"video_id":video_id},
                {
                    "$push":{
                        "comments":{"comment_id":profile_id+"_"+str(datetime.utcnow().timestamp()),"profile_id":profile_id,"channel_name":profile["channel_name"],"profile_picture":profile["profile_picture"],"comment":comment}
                    }
                }
            )
            
        else:
    
            # Add New Comment
            self.client.videos.comments.insert_one({
                "_id":video_id+"_"+str(datetime.utcnow().timestamp()),
                "video_id":video_id,
                "comments":[{"comment_id":profile_id+"_"+str(datetime.utcnow().timestamp()),"profile_id":profile_id,"channel_name":profile["channel_name"],"profile_picture":profile["profile_picture"],"comment":comment}]
            })

        return "Commented Successfully"

    def delete(self,video_comment_id,comment_id):
        if c:=self.client.videos.comments.find_one({"_id":video_comment_id}):
            self.client.videos.comments.update({"_id":video_comment_id},
                    {
                        "$pull":{
                            "comments":{"comment_id":comment_id}
                        }
                    }
                )
            return "Comment Deleted Successfully"
        return "Comment Donot Exist"

    def user_name(self, profile_id):
        return loads(dumps(self.client.auth.profile.find_one({"_id":profile_id})))["channel_name"]
    
    def video_title(self, video_id):
        return loads(dumps(self.client.videos.upload.find_one({"_id":video_id})))["title"]
    
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

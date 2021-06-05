from server.settings import clientOpen

class BaseUpload:

    def __init__(self):
        self.client = clientOpen()
    
    def create(self, profile_id ,title, description, duration, category, thumbnail, upload_file, timestamp):
        self.client.videos.upload.insert_one({
            "_id":profile_id+"_"+title+"_"+str(timestamp)+"_"+category+"_"+str(duration),
            "profile_id":profile_id,
            "title":title,
            "description":description,
            "thumbnail":thumbnail,
            "duration":duration,
            "category":category,
            "upload_file":upload_file,
            "timestamp":timestamp
        })

        self.client.close()

    def get(self, id):
        res = self.client.videos.upload.find_one({
            "_id":id
        })

        self.client.close()
        return res
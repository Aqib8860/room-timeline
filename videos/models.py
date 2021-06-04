from server.settings import clientOpen

class BaseUpload:

    def create(self, profile_id ,title, description, duration, category, thumbnail, upload_file, timestamp):
        client = clientOpen()
        client.videos.upload.insert_one({
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
        client.close()

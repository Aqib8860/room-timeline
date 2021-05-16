from server.settings import clientOpen

class BaseUpload:
    def __init__(self, id ,title, description, duration, category, thumbnail, upload_file, timestamp):
        self.profile_id=id
        self.title=title
        self.description=description
        self.thumbnail=thumbnail
        self.duration=duration
        self.category=category
        self.upload_file=upload_file
        self.timestamp=timestamp

    def create(self):
        client = clientOpen()
        client.videos.upload.insert_one({
            "profile_id":self.profile_id,
            "title":self.title,
            "description":self.description,
            "thumbnail":self.thumbnail,
            "duration":self.duration,
            "category":self.category,
            "upload_file":self.upload_file,
            "timestamp":self.timestamp
        })
        client.close()
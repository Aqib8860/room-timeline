from server.settings import category

class BaseUpload:
    def __init__(self, id ,title, description, thumbnail, duration, category, upload_file, timestamp):
        self.category=category
        
    def create(self):
        category.insert_one({
            "category":self.category,
        })
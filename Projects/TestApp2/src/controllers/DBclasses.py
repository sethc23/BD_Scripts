from google.appengine.ext import db
    
class Categories(db.Model):
    name = db.StringProperty()
    location = db.StringProperty()
    postDate = db.IntegerProperty()
    title = db.StringProperty()
    link = db.StringProperty()
    postId = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class Locations(db.Model):
    location = db.StringProperty()
    url = db.StringProperty()
    updated = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class Hierarchy(db.Model):
    location = db.StringProperty()
    category = db.StringProperty()
    url = db.StringProperty()
    random = db.IntegerProperty()
    counted = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
class PostCount(db.Model):
    city = db.StringProperty()
    category = db.StringProperty()
    postDate = db.IntegerProperty()
    postCount = db.IntegerProperty()
    entryDate = db.IntegerProperty()
    successDate = db.IntegerProperty()
    error = db.BlobProperty()
    commandUrl = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class htmlData(db.Model):
    html = db.BlobProperty()
    line = db.IntegerProperty()
    status = db.BooleanProperty()
    

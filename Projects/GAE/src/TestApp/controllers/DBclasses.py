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
    category = db.ReferenceProperty(Categories)

class CLposts(db.Model):
    location = db.ReferenceProperty(Locations)
    category = db.ReferenceProperty(Categories)

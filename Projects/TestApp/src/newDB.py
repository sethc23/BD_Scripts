from google.appengine.ext import db

class CLposts(db.Model):
    site = db.ReferenceProperty(Sites)
    category = db.ReferenceProperty(Categories)
    
class Locations(db.Model):
    location = db.StringProperty()
    category = db.ReferenceProperty(Categories)
    
class Categories(db.Model):
    postDate = db.IntegerProperty()
    title = db.StringProperty()
    link = db.StringProperty()
    postId = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)

location = "boston"    
category = "wanted"
postDate = 22809
title = "Double Jogger wanted -"
link = "testing"
postId = 1054309606

wanted = Categories(name=category, postDate=postDate,
                    title=title, link=link,
                    postId=postId)
wanted.put()

boston = Locations(location=location, category=wanted.key())
boston.put()

posts = CLposts(location=boston.key(), category=wanted.key())
posts.put()




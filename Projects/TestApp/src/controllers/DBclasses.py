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
    
class PostCount(db.Model):  # PostCount(city,category,postDate,postCount)
    city = db.StringProperty()
    category = db.StringProperty()
    postDate = db.IntegerProperty()
    postCount = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class htmlData(db.Model):
    html = db.TextProperty()
    url = db.StringProperty()
    line = db.IntegerProperty()
    status = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class errorData(db.Model):
    error = db.TextProperty()
    string1 = db.StringProperty()
    string2 = db.StringProperty()
    index = db.IntegerProperty()
    status = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class RunTimeVariable(db.Model):
    appVariable = db.StringProperty()
    A_int = db.IntegerProperty()
    B_int = db.IntegerProperty()
    A_str = db.StringProperty()
    B_str = db.StringProperty()
    C_str = db.StringProperty()
    D_str = db.StringProperty()
    E_str = db.StringProperty()
    A_bool = db.BooleanProperty()
    B_bool = db.BooleanProperty()
    A_date = db.DateTimeProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class gdataDB(db.Model):
    runStatus = db.StringProperty()
    workbook = db.StringProperty()
    stepNum = db.IntegerProperty()
    categories = db.TextProperty()
    cateNum = db.IntegerProperty()
    cities = db.TextProperty()
    cityNum = db.IntegerProperty()
    worksheet = db.StringProperty()
    WKSHstatus = db.StringProperty()
    dateHeaders = db.TextProperty()
    batchStr = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

from google.appengine.ext import db
from controllers.DBclasses import *

_DEBUG = True

def sendData(site, category, titles, links, postId, postDate, postNumber):
    try:
        line = "Start-"
        for i in range(0, postNumber):  # len(titles)):
            line = line + "entry-"
            sub_entry = Categories()
            line = line + " value: " + site
            sub_entry.location = str(site)
            line = line + " value: " + category
            sub_entry.name = str(category)
            line = line + " value: " + titles[i]
            sub_entry.title = str(titles[i])
            line = line + " value: " + links[i]
            sub_entry.link = str(links[i])
            line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
            sub_entry.postId = int(postId[i])
            line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
            sub_entry.postDate = int(postDate[i])
            try:
                line = line + "put-sub"
                sub_entry.put()
                # line = line+"put-entry"
                # entry = Locations(location=site,category=sub_entry.key())
                # entry.put()
                # line = line+"put-top"
                # top_entry = CLposts(location=entry.key(),category=sub_entry.key())
                # top_entry.put()
            except:
                line = line + "encode-"
                text = titles[i].encode('ASCII', 'elinks')
                line = line + "entry-"
                sub_entry = Categories()
                line = line + " value: " + site
                sub_entry.location = str(site)
                line = line + " value: " + category
                sub_entry.name = str(category)
                line = line + " value: " + titles[i]
                sub_entry.title = str(titles[i])
                line = line + " value: " + links[i]
                sub_entry.link = str(links[i])
                line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
                sub_entry.postId = int(postId[i])
                line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
                sub_entry.postDate = int(postDate[i])
                line = line + "put-sub"
                sub_entry.put()
                # line = line+"put-entry"
                # entry = Locations(location=site,category=sub_entry.key())
                # entry.put()
                # line = line+"put-top"
                # top_entry = CLposts(location=entry.key(),category=sub_entry.key())
                # top_entry.put()
            line = line + "iteration-"
        line = "end"
        return "success"
    except:
        receivedData = site, category, titles, links, postId, postDate, postNumber
        line = str(receivedData) + "    ----    " + line
        return "sendData failure: " + line

def checkQueryPosts(postId):
    repeatPosts = []
    if len(postId) == 0:
        return repeatPosts
    else:
        oldpostId = postId[:]
        newpostId = postId[:]
        newpostId.sort()
        small = eval(newpostId[0])
        big = eval(newpostId[len(newpostId) - 1])
        postIdQuery = Categories.gql("WHERE postId >= :1 AND postId <= :2 ORDER BY postId DESC", small, big)
        try:
            x = postIdQuery.get()
        except:
            return repeatPosts
        if postIdQuery.count() == 0:
            return repeatPosts
        postQlist = list(post.postId for post in postIdQuery)
        # print "postQlist[0] is ",postQlist[0]," is type ",str(type(str(postQlist[0])))
        # print "oldpostId[0] is ",oldpostId[0]," is type ",str(type(long(oldpostId[0])))
        for i in range(0, len(oldpostId)):
            try:
                a = postQlist.index(long(oldpostId[i]))
                repeatPosts.append(str(postQlist[a]))
            except ValueError:
                pass
        # print len(repeatPosts)
        return repeatPosts
    
def sendPostCount(location, category, postDate, count):
    line = "Start-"
    line = line + "entry-"
    sub_entry = PostCount()
    line = line + " value: " + location
    sub_entry.city = str(location)
    line = line + " value: " + category
    sub_entry.category = str(category)
    line = line + " values: " + str(postDate)
    sub_entry.postDate = int(postDate)
    line = line + " values: " + str(count)
    sub_entry.postCount = int(count)
    try:
        line = line + "put-sub"
        sub_entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendCountSchedule(url):
    line = "Start-"
    for i in range(0, len(url)):
        line = line + "entry-"
        entry = Hierarchy()
        line = line + " values: " + str(url[i])
        entry.url = str(url[i])
        try:
            line = line + "put-sub"
            entry.put()
        except:
            return "sendData failure: " + line 
        line = line + "iteration-"
    line = "end"
    return "success"

def sendOneCity(location, url):
    clean = cleanOneCity(url)
    line = "Start-"
    entry = Locations()
    line = line + " values: " + location
    entry.location = str(location)        
    line = line + " values: " + url
    entry.url = str(url)
    entry.updated = False
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def cleanOneCity(url):
    oneCityQuery = Locations.gql("WHERE url = :1", url)
    x = oneCityQuery.get()
    if x != None:
        x.delete()
        return "success"
    else:
        return "Nothing to delete"

def updateOneCity(location):
    oneCityQuery = Locations.gql("WHERE updated = False AND location = :1", location)
    try:
        x = oneCityQuery.get()
        x.updated = True
        x.put()
        return "Updated"
    except:
        return "Error in updating location status"

def sendCityCate(location, category, fullurl, random):
    clean = cleanOneCityCate(fullurl)
    line = "Start-"
    entry = Hierarchy()
    line = line + " values: " + location
    entry.location = str(location)
    line = line + " values: " + category
    entry.category = str(category)        
    line = line + " values: " + fullurl
    entry.url = str(fullurl)
    line = line + " values: " + fullurl
    entry.random = int(random)
    entry.counted = False
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def cleanOneCityCate(fullurl):
    oneCityCateQuery = Hierarchy.gql("WHERE url = :1", fullurl)
    x = oneCityCateQuery.get()
    if x != None:
        x.delete()
        return "success"
    else:
        return "Nothing to delete"

def getOneCity():
    oneCityQuery = Locations.gql("WHERE updated = False")
    x = oneCityQuery.get()
    if x != None:
        return x
    else:
        return "Nothing to Update"

def getOneCategory():
    oneCateQuery = Hierarchy.gql("WHERE counted = False")
    try:
        x = oneCateQuery.get()
        return x
    except:
        return "Nothing to Update"
    
    """
    class Hierarchy(db.Model):
    location =  db.StringProperty()
    category =  db.StringProperty()
    url = db.StringProperty()
    random = db.IntegerProperty()
    counted = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    """

def updateOneCategory(location, category):
    oneCityQuery = Hierarchy.gql("WHERE updated = False " + 
                                 "AND location = :1 " + 
                                 "AND category = :2",
                                 location, category)
    try:
        x = oneCateQuery.get()
        x.updated = True
        x.put()
        return "Updated"
    except:
        return "Error in updating location status"    

def deleteAll(database, packNum):
    count = 0
    for instance in eval(database).all():
        instance.delete()
        count = count + 1
    return "<p>" + str(count) + "</p>" + " in " + str(database) + " deleted"
    

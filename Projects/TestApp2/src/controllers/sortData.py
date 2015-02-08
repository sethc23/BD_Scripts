import getData
import queryData
from google.appengine.ext.webapp import template
import os
from google.appengine.ext import db
import debug

_DEBUG = True


def prev10(self, origFirst, pageNumber, firstPost):
    nextQuery = db.GqlQuery("SELECT * FROM Categories " + 
                              "WHERE postId > :1 " + 
                              "ORDER BY postId DESC",
                              eval(firstPost))
    pageNumber = str(int(pageNumber) - 1)
    posts = nextQuery.fetch(10, offset=int(int(pageNumber) * 10))
    if len(posts) == 0:
        return False
    else:
        firstPost = posts[0].postId
        lastPost = posts[9].postId
        if str(firstPost) == str(origFirst):  # only until new sorting methods exist, yeeks!
            prevPage = None
        else:
            prevPage = "True"
        nextPage = "True"
        template_values = {'posts': posts,
                           'origFirst' : origFirst,
                           'pageNumber' : pageNumber,
                           'firstPost' : firstPost,
                           'lastPost': lastPost,
                           'prevPage' : prevPage,
                           'nextPage': nextPage}
        return template_values

def next10(self, origFirst, pageNumber, lastPost):
    nextQuery = db.GqlQuery("SELECT * FROM Categories " + 
                              "WHERE postId < :1 " + 
                              "ORDER BY postId DESC",
                              eval(lastPost))
    if nextQuery.fetch(1, offset=10):
        nextPage = "True"
    else:
        nextPage = None
    prevPage = "True"
    posts = nextQuery.fetch(10)
    pageNumber = str(int(pageNumber) + 1)
    if len(posts) == 0:
        return False
    else:
        if len(posts) != 10:  # in case not 10 more results (saves small calculation)
            firstPost = posts[0].postId
            lastPost = posts[len(posts) - 1].postId
        else:
            firstPost = posts[0].postId
            lastPost = posts[9].postId
        template_values = {'posts': posts,
                           'origFirst' : origFirst,
                           'pageNumber' : pageNumber,
                           'firstPost' : firstPost,
                           'lastPost': lastPost,
                           'prevPage' : prevPage,
                           'nextPage': nextPage}
        return template_values

def ShowDataApp(self, location, category):  ####--------Show data on first page
    pageNumber = 1
    if location != None and category != None:
        firstQuery = db.GqlQuery("SELECT * FROM Categories " + 
                                 "WHERE location = :1 AND name = :2 " + 
                                 "ORDER BY postId DESC",
                                 location, category)
    elif location != None:
        firstQuery = db.GqlQuery("SELECT * FROM Categories " + 
                                 "WHERE location = :1 " + 
                                 "ORDER BY postId DESC",
                                 location)
    elif category != None:
        firstQuery = db.GqlQuery("SELECT * FROM Categories " + 
                                 "WHERE name = :1 " + 
                                 "ORDER BY postId DESC",
                                 category)
    else:
        pass
    posts = firstQuery.fetch(10)
    if len(posts) != 10:  # in case not 10 results (saves small calculation)
      if len(posts) == 0:
        pass
      else:
        firstPost = posts[0].postId
        lastPost = posts[len(posts) - 1].postId
    else:
      firstPost = posts[0].postId
      lastPost = posts[9].postId
    if firstQuery.fetch(1, offset=10):
      nextPage = "True"
    else:
      nextPage = None
    prevPage = None  # first page, don't need prev page button
    origFirst = firstPost
    template_values = {'posts': posts,
                       'origFirst' : origFirst,
                       'pageNumber' : pageNumber,
                       'firstPost' : firstPost,
                       'lastPost': lastPost,
                       'prevPage': prevPage,
                       'nextPage': nextPage}
    path = os.path.join(os.path.dirname(__file__), 'data_index.html')
    self.response.out.write(template.render(path, template_values))
    

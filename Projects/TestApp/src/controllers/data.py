from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
import getData, queryData, debug, sortData, htmlData, DBclasses
from DBclasses import *

_DEBUG = True

def GetDataApp(self):
    url = "http://geo.craigslist.org/iso/us"
    city = "boston"
    top_category = "for sale"
    sub_category = "wanted"
    postNum = 10
    result1 = getData.PostData(url, city, top_category, sub_category)
#    sites = result1[0]
#    categories = result1[1]
#    postTitles = result1[2]
#    self.response.out.write(str(len(postTitles)))
#    postUrls = result1[3]
#    self.response.out.write(str(len(postUrls)))
#    postId = result1[4]
#    self.response.out.write(str(len(postId)))
#    postDate = result1[5]
#    self.response.out.write(str(len(postDate)))
    postNumber = 10
    # self.response.out.write(result1) 
    result2 = queryData.sendData(result1[0], result1[1], result1[2], result1[3], result1[4], result1[5], postNumber)

def SortDataApp(self):
    origFirst = self.request.get('origFirst')  # save first post as starting point
    pageNumber = self.request.get('pageNumber')
    
    if self.request.get('Prev 10'):  # Goto prev 10
      firstPost = self.request.get('firstPost')
      template_values = sortData.prev10(self, origFirst, pageNumber, firstPost)
      if template_values == False:
          pass
      else:
          path = os.path.join(os.path.dirname(__file__), 'data_index.html')
          self.response.out.write(template.render(path, template_values))          
      
    if self.request.get('Next 10'):  # Goto next 10
      lastPost = self.request.get('lastPost')
      template_values = sortData.next10(self, origFirst, pageNumber, lastPost)
      if template_values == False:
          pass
      else:
          path = os.path.join(os.path.dirname(__file__), 'data_index.html')
          self.response.out.write(template.render(path, template_values))  

def ShowDataApp(self, location, category):  ####--------Show data on first page
    pageNumber = 0
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
        print "error getting data"
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
    try:
        origFirst = firstPost
    except:
        return self.redirect('/getdata', permanent=True)
    hier_result = self.request.get("hier_result")
    count_result = self.request.get("count_result")
    getcount_result = self.request.get("getcount_result")
    template_values = {'posts': posts,
                       'origFirst' : origFirst,
                       'pageNumber' : pageNumber,
                       'firstPost' : firstPost,
                       'lastPost': lastPost,
                       'prevPage': prevPage,
                       'nextPage': nextPage,
                       'hier_result': hier_result,
                       'count_result': count_result,
                       'getcount_result': getcount_result}
    path = os.path.join(os.path.dirname(__file__), 'data_index.html')
    self.response.out.write(template.render(path, template_values))

def MakeQueryApp(self, type, upperDB):
    if type == "get":
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'makequery_index.html')
        self.response.out.write(template.render(path, template_values))

    if type == "post":
        database = self.request.get("database")
        submit = self.request.get("submit")
        filter1 = self.request.get("filter1")
        # WHERE,ORDER,
        if database == "":
            pass
        else:
            Query = eval(database).all()
            queryProp = eval(database).properties()

                        
            template_values = {'queryProp' : queryProp}

            path = os.path.join(os.path.dirname(__file__), 'makequery_index.html')
            self.response.out.write(template.render(path, template_values))

            
        
        


        
        
        
    self.response.out.write(str(type))
#    pageNumber = 0
#    if queryString != "":
#        firstQuery = db.GqlQuery(str(queryString))
#    else:
#        pass
#    posts = firstQuery.fetch(10)
#    if len(posts) != 10:  #in case not 10 results (saves small calculation)
#      if len(posts) == 0:
#        pass
#      else:
#        firstPost = posts[0].postId
#        lastPost = posts[len(posts)-1].postId
#    else:
#      firstPost = posts[0].postId
#      lastPost = posts[9].postId
#    if firstQuery.fetch(1,offset=10):
#      nextPage = "True"
#    else:
#      nextPage = None
#    prevPage = None   #first page, don't need prev page button
#    template_values = {'posts': posts,
#                       'origFirst' : origFirst,
#                       'pageNumber' : pageNumber,
#                       'firstPost' : firstPost,
#                       'lastPost': lastPost,
#                       'prevPage': prevPage,
#                       'nextPage': nextPage}
#    path = os.path.join(os.path.dirname(__file__), 'makequery_index.html')
#    self.response.out.write(template.render(path, template_values))

def GetWebPageApp(self):
    # url = "http://geo.craigslist.org/iso/us"
    # result = htmlData.send(url)
    result = htmlData.get()
    self.response.out.write(str(result))
    
def TestPageApp(self):
#    postId = ['1055931122', '1055936205', '1055925235', '1055857553', '1055919939', '1055918263', '1055919004', '1055843716']
#    result = queryData.checkQueryPosts(postId)
#    self.response.out.write("checkQueryPosts: "+str(result))
    result = debug.getData()

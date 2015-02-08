from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
from postCount import topCount
from queryData import sendPostCount, sendOneCity, getOneCity, updateOneCity, updateOneCategory
from postCountSch import getCities, getCategories  # ,setHierarchy
from postCountSch import setPostSchedule, runCateCount, cleanSchedule

def GetPostCountApp(self):
    if str(action) == "schedule":
        section = getOneCategory()
        if str(city) == "Nothing to Update":
            return "counted"
        else:
            return "counting schedule done"
        postDate, postCount = runCateCount(full_url)
        city = section.location
        category = section.category
        fullurl = section.url
        if str(result) == "success":
            update_result = updateOneCategory(location, category)
            if str(update_result) == "Updated":
                return "success"
            else:
                return str("<p>" + "count success, updating failure" + "</p>")
        else:
            # TODO: error handling
            return str(result)

""" 
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

    
    
    location = self.request.get('location')
    category = self.request.get('category')
    full_url = self.request.get('fullurl')
    postDate,count = putCateCount(full_url) #for yesterday
    result2 = sendPostCount(location,category,postDate,count)
    
    self.response.out.write("<p>"+str(result2)+"</p>")
 """
    
def SortPostCountApp(self):
    origFirst = self.request.get('origFirst')  # save first post as starting point
    pageNumber = self.request.get('pageNumber')
    
    if self.request.get('Prev 10'):  # Goto prev 10
      firstPost = self.request.get('firstPost')
      template_values = sortData.prev10(self, origFirst, pageNumber, firstPost)
      if template_values == False:
          pass
      else:
          path = os.path.join(os.path.dirname(__file__), 'research_index.html')
          self.response.out.write(template.render(path, template_values))          
      
    if self.request.get('Next 10'):  # Goto next 10
      lastPost = self.request.get('lastPost')
      template_values = sortData.next10(self, origFirst, pageNumber, lastPost)
      if template_values == False:
          pass
      else:
          path = os.path.join(os.path.dirname(__file__), 'research_index.html')
          self.response.out.write(template.render(path, template_values))  

def ShowPostCountApp(self, city, category):  ####--------Show data on first page
    pageNumber = 0
    firstQuery = db.GqlQuery("SELECT * FROM PostCount ORDER BY postCount DESC")

    posts = firstQuery.fetch(50)
    
    template_values = {'posts': posts}
    path = os.path.join(os.path.dirname(__file__), 'research_index.html')
    self.response.out.write(template.render(path, template_values))

def SetHierarchyApp(self, action, specific):
    if str(action) == "cities":
        x = getCities(None, False)  # send url,random - return result
        result = []
        for i in range(0, len(x[0])):
            z = sendOneCity(str(x[0][i]), str(x[1][i]))  # return location,url
            result.append(z)
            if z != "success":
                break
        if z != "success":
            return "Error" + str(z)
        if result.count("success") == len(result):
            return "success"
        else:
            return ("<p>" + str(result) + "</p>")
    
    if str(action) == "deleteAll":
        self.response.out.write("<p>" + "deleting " + str(specific) + "</p>")
        result = cleanSchedule(specific)
        return result
    
    if str(action) == "categories":
        city = getOneCity()
        if str(city) == "Nothing to Update":
            return "update hierarchy done"
        y = getCategories(city.url, None, False)  # (cityurl,top_category,random),return cate_names, full_cate_urls
        result = []
        for j in range(0, len(y[0])):
            location = city.location
            category = y[0][j]
            fullurl = y[1][j]
            z = setPostSchedule(location, category, fullurl)
            result.append(z)
        if result.count("success") == len(result):
            update_result = updateOneCity(city.location)
            if str(update_result) == "Updated":
                return "success"
            else:
                return str("<p>" + "Hierarchy success, not Location Success" + "</p>")
        else:
            return str(result)

def TestPageApp(self):
#    HierarchyQuery = db.GqlQuery("SELECT * FROM Hierarchy ORDER BY created")
#    posts = firstQuery.fetch(50)
#    for i in range(0,50):
#        self.response.out.write(str(posts.url)+"<br>")
    pass

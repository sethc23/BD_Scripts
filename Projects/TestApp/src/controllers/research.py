from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
from postCountSch import getCities, getCategories, setPostSchedule, cleanSchedule
from queryData import updateOneCity, updateOneCategory, updateWebPage
from queryData import checkCityUrl, checkCityCateUrl, sendOneCity, getOneCity
from queryData import checkVariable
from queryData import getNewCategory, sendPostCount, updateOneCategory
from postCountSch import runCateCount
from queryData import sendPostCount
from errorControl import sendErrorApp
from time import time

def GetPostCountApp(self, action):
    now = int(time())
    end = now + (25)
    reset = False
    attempts = 10
    #================
    #    maximize time to run process
    #================ 
    while end >= now and attempts != 0:
        #================
        #    check for error action
        #================ 
        if action == "senderror":
            result = sendErrorApp("GetPostCount")
            if result == "success":
                action = "start"
            else:
                status = "error: GetPostCount - sendError: " + str(result)
                break
        #================
        #    check for variables
        #================ 
        appVariable = "runCateCount"
        checkPrevious = checkVariable(appVariable)
        if checkPrevious == False:
            section = getNewCategory()
            if str(section) == "Nothing to Update":
                section = getNewCategory()
                if str(section) == "Nothing to Update":
                    return "redirect-/?getcount_result=Get+Post+Count+complete"
            location = section.location
            category = section.category
            currentUrl = section.url
            action = "start"
        else:
            action = checkPrevious.A_str
            currentCount = checkPrevious.A_int
            currentUrl = checkPrevious.B_str
            indexPost = checkPrevious.C_str
            toDate = checkPrevious.D_str
            fromDate = checkPrevious.E_str
        #================
        #    run steps with or without variables
        #================
        if action == "" or action == None or action == "start":
            action = "start"
            variables = location, category
            result = runCateCount(currentUrl, action, variables)
            status = str(result)
        elif str(action) == "step1" or str(action) == "step2":
            variables = str(currentCount), currentUrl, indexPost, fromDate, toDate
            result = runCateCount(currentUrl, action, variables)
            status = str(result) 
        else:
            status = "error: GetPostCount - action: " + str(action) + "- no steps to run?"
            break
        #================
        #    FINISHED!
        #================
        if status.find('run again') != 0:
            reset = True
            break
        now = int(time())
        attempts = attempts - 1
    if status.find('run again') == 0:
        return "run again"
    else:
        return "error: " + str(status)



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
        url = "http://geo.craigslist.org/iso/us"
        x = getCities(None, "startLine")  # send url,action
        if str(x).find("run again - webpage saved") != -1:
            return "run again"
        elif str(x).find("sendDate failure") != -1:
            return x    
        elif len(x) == 3:
            sites, siteUrls, startLine = x
        maxNum = 10
        result = []
        for i in range(startLine, len(sites)):
            tempUrl = checkCityUrl(sites[i], siteUrls[i])  # None or exists (T/F) {T/F is set by category check}
            if tempUrl == None:
                dbSend = sendOneCity(sites[i], siteUrls[i])  # return location,url
                maxNum = maxNum - 1
                result.append(dbSend)
                if dbSend != "success":
                    return "Error" + str(dbSend)
            endIndex = i
            if maxNum == 0:
                break
        if result.count("success") == len(result) and endIndex != len(sites) - 1:
            updateLine = updateWebPage(url, endIndex)
            return "run again"
        else:
            delete = getCities(None, "cleanData")
            return "redirect-/?hier_result=cities+complete"
    
    if str(action) == "deleteAll":
        result = cleanSchedule(specific)
        if str(result) == "data deleted":
            return "run again"
        else:
            return "redirect-/?hier_result=" + str(specific) + "+deleted"
        
    
    if str(action) == "categories":
        city = getCategories(None, None, None)  # {cityurl,top_category,action}
        if str(city) == "update hierarchy done":  # and "Hierarchy success, not location success"
            return "redirect-/?hier_result=categories+complete"
        elif len(city) == 3:
            cityname, cate_names, full_cate_urls = city
        # get webpage,bounce,get links
        result = []
        for j in range(0, len(cate_names)):
            category = cate_names[j]
            fullurl = full_cate_urls[j]
            checkUrl = checkCityCateUrl(fullurl)  # "status:True" exists or "False"
            if checkUrl == False:
                sendCateUrl = setPostSchedule(cityname, category, fullurl)
                result.append(sendCateUrl)  # TODO: setup mechanism to change random numbers

        if result.count("success") == len(result):
            update_result = updateOneCity(cityname, None)
            if str(update_result) == "Updated":
                anotherCity = getOneCity()
                if str(anotherCity) == "Nothing to Update":
                    return "redirect-/?hier_result=categories+complete"
                else:
                    return "run again"
            else:
                return "run again"
        return str(result)

def TestPageApp(self):
#    HierarchyQuery = db.GqlQuery("SELECT * FROM Hierarchy ORDER BY created")
#    posts = firstQuery.fetch(50)
#    for i in range(0,50):
#        self.response.out.write(str(posts.url)+"<br>")
    pass

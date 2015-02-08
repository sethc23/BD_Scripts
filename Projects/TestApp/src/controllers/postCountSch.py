'''
Created on Mar 5, 2009

@author: sethchase
'''
from postCount import getHierarchy, makeRandom, getSiteUrls, getLocationSubCate
from postCount import make2Random, getPostCount, convertCLTime, convertDBTime
from queryData import sendCountSchedule, sendOneCity, deleteAll, sendCityCate
from queryData import checkWebPage, deleteWebPage, getOneCity
from queryData import checkVariable, updateVariable, sendVariable, deleteRuntimeVar
from queryData import getOneCategory, checkPostCount, updateOneCategory, sendPostCount
from htmlData import saveWebPage
from time import strftime, localtime, time, gmtime
from random import randrange

def getCities(url, action):
    if url == None:
        url = "http://geo.craigslist.org/iso/us"
    webpage = checkWebPage(url)
    if webpage == False:
        save = saveWebPage(url)
        if str(save).find("success") == 0:
            return "run again - webpage saved"
        else:
            return "print -" + str(save)
    startLine = webpage.line
    result = getSiteUrls(webpage.html)
    if str(action) == "startLine":
        sites, siteUrls = result
        return sites, siteUrls, startLine
    elif str(action) == "random":
        result = make2Random(result[0], result[1])
    elif str(action) == "cleanData":
        result = deleteWebPage(url)
    return result

def getCategories(cityurl, top_category, action):
    if cityurl == None:
        site = getOneCity()
        if str(site) == "Nothing to Update":
            return "update hierarchy done"
        cityurl = site.url
        cityname = site.location
    if top_category == None:
        top_category = "for sale"
    cate_names, sub_cate_urls = getLocationSubCate(cityurl, top_category)
    full_cate_urls = []
    for i in range(0, len(sub_cate_urls)):
        full_cate_urls.append(cityurl + sub_cate_urls[i])
    if str(action) == "None":
        result = cityname, cate_names, full_cate_urls
        return result
    result = cate_names, full_cate_urls
    if str(action) == "random":
        result = make2Random(cate_names, full_cate_urls)
        return result

def setPostSchedule(location, category, url):
    if category == None:
        result = sendOneCity(location, url)
        return result
    else:
        random = randrange(0, 999999)
        result = sendCityCate(location, category, url, random)
        return result

def postDateRange():
    timeZone = (60 * 60 * 6)  # subtract 5 hours add daylight savings from localtime
    day = (60 * 60 * 24)
    # yesterday = strftime("%a %b %d",localtime(time()-day-timeZone)) 
    # today = strftime("%a %b %d",localtime(time()-timeZone))
    yesterday = strftime("%a %b %d", localtime(time() - timeZone - day * 2))
    today = strftime("%a %b %d", localtime(time() - timeZone - day))
    fromDate = yesterday
    toDate = today
    return fromDate, toDate

def runCateCount(currentUrl, action, variables):  # for yesterday
    appVariable = "runCateCount"
    #================
    #    get results
    #================
    if str(action) == "start":
        location, category = variables
        fromDate, toDate = postDateRange()
        dateVar = fromDate, toDate
        postVariables = currentUrl, fromDate, toDate
        postDate = convertCLTime(toDate)
        checkPosts = checkPostCount(location, category, postDate)
        if checkPosts != False:
            updated = updateOneCategory(location, category)
            if str(updated) != "Updated":
                return "error: runCateCount update hierarchy error"
            return "run again"
        actionR, data1, data2 = getPostCount(postVariables, "start")

    elif str(action) == "step1" or str(action) == "step2":
        VarCount, currentUrl, indexPost, fromDate, toDate = variables
        postVariables = variables
        actionR, data1, data2 = getPostCount(postVariables, action)
        if str(actionR) == "count zero" or str(actionR) == "complete":
            s = currentUrl.find(".org/") + 5
            e = currentUrl.find("/", s) + 1
            fullurl = currentUrl[:e]
            hierarchyVar = getOneCategory(fullurl)
            location = hierarchyVar.location
            category = hierarchyVar.category
    else:
        return "error: runCateCount -end" + str(action)
            
    #================
    #    send complete results
    #================
    # currentUrl = data1
    postDate = convertCLTime(toDate)
    if str(actionR) == "count zero" or str(actionR) == "complete":
        if str(actionR) == "count zero":
            postCount = 0
        else:
            postCount = int(data2)
        sendCount = sendPostCount(location, category, postDate, postCount)
        if str(sendCount) != "success":
            return "error: runCateCount sendCount error"
        checkPrevious = checkVariable(appVariable)
        if checkPrevious != False:
            deleted = deleteRuntimeVar(appVariable)
            if str(deleted) != "variable deleted":
                return "error: runCateCount - deleting runtime variable failed", "", "" 
        updated = updateOneCategory(location, category)
        if str(updated) != "Updated":
            return "error: runCateCount update hierarchy error"
        return "run again"
    
    elif str(actionR) == "step1" or str(actionR) == "step2":
            actionR, currentUrl, indexInfo = actionR, data1, data2
            indexPost, currentCount = data2
            checkPrevious = checkVariable(appVariable)
            if checkPrevious == False:
                makeVariable = sendVariable(appVariable, currentCount, 0, actionR, currentUrl, indexPost, toDate, fromDate, None, True, None)
                if str(makeVariable) != "success":
                    return "error: runCateCount - creating runtime variable failed", "", ""
            else:
                updated = updateVariable(appVariable, currentCount, 0, actionR, currentUrl, indexPost, toDate, fromDate, None, True, None)
                if str(updated) != "Updated":
                    return "error: runCateCount - updating runtime variable failed", "", ""               
            return "run again"
    else:
        return ("error: runCateCount: " + "action: " + str(actionR) + ' - ' + str(action) + 
                " -data1: " + str(data1) + " -date2: " + str(data2)), "", ""


def cleanSchedule(datebase):
    result = deleteAll(datebase, 40)  # (datebase,fetchNum)
    return result
    
    

'''
Created on Mar 5, 2009

@author: sethchase
'''
from postCount import getHierarchy, makeRandom, getSiteUrls, getLocationSubCate
from postCount import make2Random, getPostCount, convertTime
from queryData import sendCountSchedule, sendOneCity, deleteAll, sendCityCate
from time import strftime, localtime, time, gmtime
from random import randrange


# def setHierarchy(url,top_category): #check hierarchy, return full urls in text file
#    if url == None:
#        url = "http://geo.craigslist.org/iso/us"
#    if top_category == None:
#        top_category = "for sale"
#    full_sub_url = getHierarchy(url,None,top_category)
#    #sub_category_names,sub_categories_urls = sub_categories_array
#    rand_sub_url = makeRandom(full_sub_url)
#    #result = sendCountSchedule(rand_sub_url)
#    return rand_sub_url

def getCities(url, random):  # check hierarchy, return full urls in text file
    if url == None:
        url = "http://geo.craigslist.org/iso/us"
    result = getSiteUrls(url)
    # cityNames, cityUrls = result
    if str(random) == "True":
        result = make2Random(result[0], result[1])
    return result
    
def getCategories(cityurl, top_category, random):  # check hierarchy, return full urls in text file
    if cityurl == None:
        cityurl = "http://boston.craigslist.org/"
    if top_category == None:
        top_category = "for sale"
    cate_names, sub_cate_urls = getLocationSubCate(cityurl, top_category)
    full_cate_urls = []
    for i in range(0, len(sub_cate_urls)):
        full_cate_urls.append(cityurl + sub_cate_urls[i])
    result = cate_names, full_cate_urls
    if str(random) == "True":
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

def runCateCount(full_url):  # for yesterday
    yesterday = strftime("%a %b %d", localtime(time() - (60 * 60 * 24) - (60 * 60 * 5)))
    today = strftime("%a %b %d", localtime(time() - (60 * 60 * 5)))
    yesterday = strftime("%a %b %d", localtime(time() - (60 * 60 * 24 * 2)))
    today = strftime("%a %b %d", localtime(time() - (60 * 60 * 24 * 1)))
    fromDate = yesterday 
    toDate = today
    postDate = convertTime(fromDate)
    count = getPostCount(full_url, fromDate, toDate)
    return postDate, count

def cleanSchedule(datebase):
    result = deleteAll(datebase, None)  # (datebase,fetchNum)
    return result
    
    

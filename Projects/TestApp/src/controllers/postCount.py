import urllib2
import BeautifulSoup
from random import randrange
from time import strptime, strftime
from getData import getSiteUrls

def convertCLTime(CLformat):
    struct_time = strptime(CLformat + " 2009", "%a %b %d %Y")
    CLformat = strftime("%m%d%y", struct_time)
    return CLformat

def convertDBTime(DBformat):
    struct_time = strptime(DBformat, "%m%d%y")
    DBformat = strftime("%a %b %d", struct_time)
    return DBformat

def getLocationLinks(url):
  result = urllib2.urlopen(url)
  HTML = result.read()
  HTML = unicode(HTML, "iso-8859-1").encode("ASCII", 'ignore')
  links = BeautifulSoup.BeautifulSoup(HTML).findAll("a")
  return links

def getSiteUrls(webpage):
  links = BeautifulSoup.BeautifulSoup(webpage).findAll("a")
  sites, siteUrls = [], []
  for url in range(0, len(links)):
    try:
        temp1 = str(links[url].string)
        temp2 = str(links[url].get('href'))
        if temp1 == "None":
            temp1 = links[url].b.string
    except:
        x = str(links[url])
        z = str(x)
        s1 = z.find('href=') + 5
        e = z.find('"', s1)
        temp1 = z[s1:e]
        s2 = z.find('>', e) + 1
        e2 = z.find('>', s2)
        temp2 = z[s2:e2]
    sites.append(temp1)
    siteUrls.append(temp2)
    if temp1 == None:
      del sites[len(sites) - 1]
      del siteUrls[len(siteUrls) - 1]
    if temp2.find('www.craigs') == 7:
      del sites[len(sites) - 1]
      del siteUrls[len(siteUrls) - 1]
    if temp2.find('forums.craigs') == 7:
      del sites[len(sites) - 1]
      del siteUrls[len(siteUrls) - 1]
    if temp2.find('en.wikipedia') == 7:
      del sites[len(sites) - 1]
      del siteUrls[len(siteUrls) - 1]
  return sites, siteUrls

def getLocationUrl(url, city):
    line = "getLocations->"
    line = line + "getSiteUrls-"
    sites, siteUrls = getSiteUrls(url)
    line = line + "Loc_index-"
    Loc_index = sites.index(city)
    line = line + "Location_Url-"
    Location_Url = siteUrls[Loc_index]
    return Location_Url

def getLocationSubCate(location_url, top_category):
    HTML = urllib2.urlopen(location_url).read()
    checkTags = testHTML(HTML, location_url)
    while checkTags != True:
        HTML = fixHTML(HTML)
        checkTags = testHTML(HTML, location_url)
    HTML = unicode(HTML, "iso-8859-1").encode("ASCII", 'ignore')
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    siteHTML = str(siteHTML).replace("\n", "")
    siteHTML = BeautifulSoup.BeautifulSoup(siteHTML)
    subList = siteHTML.find('div', id="sss")
    subLinks = subList.findChildren('a')
    categories, subUrls = getCategories(subLinks)
    if categories.count(top_category) != -1:
        indexNum = categories.index(top_category)
        categories.pop(indexNum)
        subUrls.pop(indexNum)
    return categories, subUrls

def getCategories(self):
  categText, categUrls = [], []
  for url in range(0, len(self)):
    temp1 = str(self[url].string)
    categText.append(temp1)
    temp2 = str(self[url].get('href'))
    categUrls.append(temp2)
  if len(categText) == len(categUrls):
    return categText, categUrls

def nextPage(siteHTML, baseUrl, date):
    try:
      test = siteHTML.find('a', text='next 100 postings')
      footer = siteHTML.find('p', align='center')
      nextPageUrl = footer.findChild('a').get('href')
    except:
      return siteHTML, None
    newUrl = baseUrl + nextPageUrl
    HTML = urllib2.urlopen(newUrl).read()
    checkTags = testHTML(HTML, newUrl)
    while checkTags != True:
        HTML = fixHTML(HTML)
        checkTags = testHTML(HTML, newUrl)
    HTML = unicode(HTML, "iso-8859-1").encode("ASCII", 'ignore')
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    siteHTML = str(siteHTML).replace("\n", "")
    newHTML = BeautifulSoup.BeautifulSoup(siteHTML)
    return  newHTML, newUrl

def StartDateHTML(fromDate, toDate, checkDates, allDates, siteHTML, currentUrl):
    if str(checkDates).find("error") == 0:
        return checkDates, "", ""
    elif str(checkDates) == "count zero":
        action = "count zero"
        postCount = 0
        return action, currentUrl, postCount  # counting is different for different steps
    elif str(checkDates) == "next page":
        action = "next page"
        newestOldDate = nextOldestDate(fromDate, toDate, allDates)
        if newestOldDate == None:
            action = "count zero"
            postCount = 0
            return action, currentUrl, postCount
        else:
            postList = siteHTML.findAll('p')
            del postList[len(postList) - 1]
            indexPost = postList[len(postList) - 1]
            currentCount = 0
            indexInfo = indexPost, currentCount
            return action, currentUrl, indexInfo
    elif str(checkDates) == "make count" or str(checkDates) == "fromDate" or str(checkDates) == "toDate" :
        begin = siteHTML.find('h4', text=toDate)
        if begin == None:
            action = "count zero"
            postCount = 0
            return action, currentUrl, postCount
        postList = siteHTML.findAll('p')
        del postList[len(postList) - 1]
        end = siteHTML.find('h4', text=fromDate)
        if end == None:
            newestOldDate = nextOldestDate(fromDate, toDate, allDates)
            if newestOldDate != None:
                lastDate = convertDBTime(newestOldDate)
                end = siteHTML.find('h4', text=lastDate)
        if end != None:
            startCount = postList.index(begin.next) + 1
            endCount = postList.index(end.previous.previousSibling)
            postCount = endCount - startCount + 2
            action = "complete"
            return action, currentUrl, postCount
        else:
            action = "step2"
            startPost = postList.index(begin.next)
            indexPost = postList[len(postList) - 1]
            currentCount = len(postList) - startPost
            indexInfo = indexPost, currentCount
            return action, currentUrl, indexInfo
    else:
        return "error:datecheck " + str(action), None, None

def findIndexPost(currentUrl, indexPost, baseUrl, findDate):
    HTML = urllib2.urlopen(currentUrl).read()
    checkTags = testHTML(HTML, currentUrl)
    while checkTags != True:
        HTML = fixHTML(HTML)
        checkTags = testHTML(HTML, currentUrl)
    HTML = unicode(HTML, "iso-8859-1").encode("ASCII", 'ignore')
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    siteHTML = str(siteHTML).replace("\n", "")
    siteHTML = BeautifulSoup.BeautifulSoup(siteHTML)
    indexHTML = BeautifulSoup.BeautifulSoup(indexPost).find('p')
    postList = siteHTML.findAll('p')
    del postList[len(postList) - 1]
    # seek indexPost
    startIndex = postList.count(indexHTML)
    if startIndex != 0:
        startIndex = postList.index(indexHTML)
    elif startIndex == 0:
        siteHTML, newUrl = nextPage(siteHTML, baseUrl, findDate)
        if newUrl != None:
            currentUrl = newUrl
        postList = siteHTML.findAll('p')
        del postList[len(postList) - 1]
        if postList.count(indexHTML) != 0:
            startIndex = postList.count(indexHTML)
        else:
            return ("error: findIndexPost: at URL: " + str(currentUrl) + 
                    " & baseUrl: " + str(baseUrl) + ' - '), str(baseUrl), ("--" + str(indexPost) + "--")
    return siteHTML, currentUrl, startIndex

def getPostCount(variables, action):
    if str(action) == "start":
        currentUrl, fromDate, toDate = variables
        HTML = urllib2.urlopen(currentUrl).read()
        checkTags = testHTML(HTML, currentUrl)
        while checkTags != True:
            HTML = fixHTML(HTML)
            checkTags = testHTML(HTML, currentUrl)
        HTML = unicode(HTML, "iso-8859-1").encode("ASCII", 'ignore')
        siteHTML = BeautifulSoup.BeautifulSoup(HTML)
        siteHTML = str(siteHTML).replace("\n", "")
        siteHTML = BeautifulSoup.BeautifulSoup(siteHTML)   
        begin = siteHTML.find('h4', text=toDate)
        e = currentUrl.find('index')
        if e != -1:
            baseUrl = currentUrl[:e]
        else:
            baseUrl = currentUrl
        if begin == None:
            siteHTML, newUrl = nextPage(siteHTML, baseUrl, toDate)
            if newUrl != None:
                currentUrl = newUrl
        allDates = siteHTML.findAll('h4')
        startDate = convertCLTime(fromDate)
        endDate = convertCLTime(toDate)
        if len(allDates) == 0:
            return "count zero", currentUrl, ""
        checkDates = dateCheck(startDate, endDate, allDates)
        action, data1, data2 = StartDateHTML(fromDate, toDate, checkDates, allDates, siteHTML, currentUrl)
        if str(action) == "next page":
            action = "step1"
        return action, data1, data2
        # count zero,fromDate,make count,toDate,next page
    elif str(action) == "step1":
        currentCount, currentUrl, indexPost, fromDate, toDate = variables
        postCount = currentCount
        e = currentUrl.find('index')
        if e != -1:
            baseUrl = currentUrl[:e]
        else:
            baseUrl = currentUrl
        siteHTML, currentUrl, startIndex = findIndexPost(currentUrl, indexPost, baseUrl, toDate)
        if siteHTML.find("error:") == 0:
            return siteHTML, currentUrl, startIndex  # error for not finding startIndex
        # indexPost Exists, so...
        begin = siteHTML.find('h4', text=toDate)
        # startPost not exist, so go to next page
        if begin == None:
            siteHTML, newUrl = nextPage(siteHTML, baseUrl, toDate)
            if newUrl != None:
                currentUrl = newUrl
            begin = siteHTML.find('h4', text=toDate)
        postList = siteHTML.findAll('p')
        del postList[len(postList) - 1]
        # startPost still not exist...check for later date ??{should change next oldest date, maybe begin not there, but end is}
        allDates = siteHTML.findAll('h4')
        startDate = convertCLTime(fromDate)
        endDate = convertCLTime(toDate)
        checkDates = dateCheck(startDate, endDate, allDates)
        action, data1, data2 = StartDateHTML(fromDate, toDate, checkDates, allDates, siteHTML, currentUrl)
        if str(action) == "next page":
            action = "step1"
        return action, data1, data2
    
    elif str(action) == "step2":
        currentCount, currentUrl, indexPost, fromDate, toDate = variables
        postCount = currentCount
        e = currentUrl.find('index')
        if e != -1:
            baseUrl = currentUrl[:e]
        else:
            baseUrl = currentUrl
        siteHTML, currentUrl, startIndex = findIndexPost(currentUrl, indexPost, baseUrl, fromDate)
        if str(siteHTML).find("error:") == 0:
            return siteHTML, currentUrl, startIndex  # error for not finding startIndex
        # indexPost Exists, so...
        end = siteHTML.find('h4', text=fromDate)
        # endPost not exist, go to next page
        if end == None:
            postCount = int(currentCount) + (100 - startIndex) - 1
            siteHTML, newUrl = nextPage(siteHTML, baseUrl, fromDate)
            if newUrl != None:
                currentUrl = newUrl
            end = siteHTML.find('h4', text=fromDate)
        postList = siteHTML.findAll('p')
        del postList[len(postList) - 1]
        # endPost still not exist...check for later date 
        if end == None:
            allDates = siteHTML.findAll('h4')
            newestOldDate = nextOldestDate(fromDate, toDate, allDates)
            if newestOldDate != None:
                lastDate = convertDBTime(newestOldDate)
                end = siteHTML.find('h4', text=lastDate)
        # endPost exist NOW or BEFORE
        if end != None:
            if len(end.previous.previousSibling.findAll('td')) == 0:
                endPostIndex = postList.index(end.previous.previousSibling)
                postCount = int(postCount) + endPostIndex + 1  # not neccessarily!
            else:
                postCount = int(postCount)
            action = "complete"
            return action, currentUrl, postCount
        else:
            # not anywhere, so 
            # (handle "count zero","next page"//error with "toDate", "make count", "fromDate") 
            # count zero,fromDate,make count,toDate,next page
            action = "step2"
            indexPost = postList[len(postList) - 1]
            currentCount = postCount + 100
            indexInfo = indexPost, currentCount
            return action, currentUrl, indexInfo
    else:
        return "error: getPostCount - not sure what step", "", ""

def topCount(url, city, top_category, fromDate, toDate):
    location_url = getLocationUrl(url, city)
    sub_categories_array = getLocationSubCate(location_url, top_category)
    sub_category_names, sub_categories_urls = sub_categories_array
    DBformatDate = convertCLTime(toDate)
    postCount, postDate = [], []
    for i in range(0, len(sub_categories_array[1])):
      baseUrl = location_url + sub_categories_urls[i]
      count = getPostCount(baseUrl, fromDate, toDate)
      if type(count) is str:
        return "trouble with CyclePostPages- ", count, sub_category_names[i]
      else:
        postCount.append(count)
      postDate.append(DBformatDate)
    if len(sub_categories_array[0]) != len(sub_categories_array[1]):
        return "sub_category_array mismatch", sub_category_names[i], []
    return city, sub_category_names, postDate, postCount

def subCount(city, top_category, sub_category_array, fromDate, toDate):  # sub_category_name,sub_categories_url = sub_category_array
    sub_category_name, sub_categories_url = sub_category_array
    DBformatDate = convertCLTime(toDate)
    postCount, postDate = [], []
    baseUrl = location_url + sub_categories_urls[i]
    count = getPostCount(baseUrl, fromDate, toDate)
    if type(count) is str:
      return "trouble with CyclePostPages- ", count, sub_category_names[i]
    else:
      postCount.append(count)
    postDate.append(DBformatDate)   
    return city, sub_category_names, postDate, postCount

def getHierarchy(url, city, top_category):
    if city != None:
        location_url = getLocationUrl(url, city)
        sub_categories_array = getLocationSubCate(location_url, top_category)
        # sub_category_names,sub_categories_urls = sub_categories_array
        return sub_categories_urls
    else:
        sites, siteUrls = getSiteUrls(url)
        # sub_categories_array = [],[]
        full_sub_url = []
        for i in range(0, len(sites)):
           newSubData = getLocationSubCate(siteUrls[i], top_category)
           # sub_categories_array[0].extend(newSubData[0])
           # sub_categories_array[1].extend(newSubData[1])
           for j in range(0, len(newSubData[1])):
               full_sub_url.append(siteUrls[i] + newSubData[1][j])
        return full_sub_url

def makeRandom(some_list):
    a = some_list
    b = []
    c = []
    for i in range(0, len(a)):
      c.append(randrange(1, 1000))
    d = c[:]
    d.sort()
    for i in range(0, len(a)):
      b.append(c.index(d[i]))
    x = []
    for j in range(0, len(a)):
        x.append(a[b[j]])
    return x

def make2Random(listA, listB):
    a = makeRandom(listA)
    x = [], []
    for j in range(0, len(listA)):
        listA.index(a[j])
        x[0].append(listA[listA.index(a[j])])
        x[1].append(listB[listA.index(a[j])])
    return x

def dateCheck(fromDate, toDate, allDates):
    dateList = []
    for date in allDates:
        if date.string != None:
            tempDate = convertCLTime(str(date.string))
            dateList.append(tempDate)
    dateList.sort()
    if len(dateList) > 0:
        newest = dateList[len(dateList) - 1]
    else:
        newest = dateList[0]
    oldest = dateList[0]
    if oldest < fromDate and newest < fromDate :  # too old
        return "count zero"
    elif oldest > toDate and newest > toDate:  # too new
        return "next page"  # keep going back
    elif oldest < fromDate and newest < toDate :  # fromDate
        return "fromDate"
    elif oldest == fromDate:
        return "fromDate"
    elif fromDate < oldest and toDate < newest:  # toDate
        return "toDate"
    elif newest == toDate:
        return "toDate"
    elif oldest < fromDate or toDate < newest:  # both on page
        return "make count"
    else:
        return "error: datecheck - unknown dates"

def nextOldestDate(startDate, endDate, allDates):
    startDate = convertCLTime(startDate)
    endDate = convertCLTime(endDate)
    for date in allDates:
        if date.string != None:
            tempDate = convertCLTime(str(date.string))
            if int(tempDate) < int(startDate):  # and tempDate < fromDate:
                nextOldest = (tempDate)
                break
    try:
        return nextOldest
    except:
        return None

def testHTML(HTML, currentUrl):
    HTML2 = urllib2.urlopen(currentUrl).readlines()
    A = HTML.count("<")
    B = HTML.count(">")
    if A != B:
        return HTML2
    else:
        return True

def fixHTML(HTML):
    ind1 = []
    ind2 = []
    end = False
    pt = 0
    ptB = 0
    while end == False:
        if HTML.find("<", pt) != -1:
            pt2 = HTML.find("<", pt)
            ind1.append(pt2)
            pt = pt2 + 1
        elif HTML.find(">", ptB) != -1:
            pt2B = HTML.find(">", ptB)
            ind2.append(pt2B)
            ptB = pt2B + 1
        else:
            end = True
    A = len(ind1)
    B = len(ind2)
    if A > B:
        for i in range(0, B):
            left = ind1[i + 1]
            right = ind2[i]
            if left < right:
                deleteChar = ind1[i]
                break
    if B > A:
        for i in range(0, A):
            left = ind2[i + 1]
            right = ind1[i]
            if left < right:
                deleteChar = ind2[i]
                break
    HTML = str(HTML[0:deleteChar]) + str(HTML[deleteChar + 1:len(HTML)])
    return HTML

def test1():  # Check full hierarchy, get post count
  ####################
  url = "http://geo.craigslist.org/iso/us"
  city = "boston"
  top_category = "for sale"
  fromDate = "Sun Mar 01" 
  toDate = "Mon Mar 02"
  result = topCount(url, city, top_category, fromDate, toDate)
  city, sub_category_names, postDate, postCount = result
  ####################
  return result




import urllib2
import BeautifulSoup
from random import randrange
import time
from getData import getSiteUrls

def convertTime(CLformat):
    struct_time = time.strptime(CLformat + " 2009", "%a %b %d %Y")
    DBformat = time.strftime("%m%d%y", struct_time)
    return DBformat

def getLocationLinks(url):
  result = urllib2.urlopen(url)
  html = result.read()
  links = BeautifulSoup.BeautifulSoup(html).findAll("a")
  return links

def getSiteUrls(url):
  links = getLocationLinks(url)
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

def getLocationSubCate(location, top_category):
  HTML = urllib2.urlopen(location).read()
  siteHTML = BeautifulSoup.BeautifulSoup(HTML)
  subList = siteHTML.find('table', summary=top_category)
  subLinks = subList.findChildren('a')
  categories, subUrls = getCategories(subLinks)
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
      return False, siteHTML

    # wait(1)
    HTML = urllib2.urlopen(baseUrl + nextPageUrl).read()
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    postDate = siteHTML.findAll('h4', text=date)
    return  postDate, siteHTML

def getPostCount(baseUrl, fromDate, toDate):
  HTML = urllib2.urlopen(baseUrl).read()
  siteHTML = BeautifulSoup.BeautifulSoup(HTML)
  begin = siteHTML.findAll('h4', text=toDate)
  repeatMax = 100
  while begin == [] and repeatMax != 0:
      begin, siteHTML = nextPage(siteHTML, baseUrl, toDate)
      repeatMax = repeatMax - 1
  if begin == False or repeatMax == 0:
    # print "couldn't find starting post"
    return "couldn't find starting post" + str(siteHTML)
  begin = siteHTML.find('h4', text=toDate)
  end = siteHTML.find('h4', text=fromDate)
  postList = siteHTML.findAll('p')
  if end == None:
    del postList[len(postList) - 1]
    # print postList[postList.index(begin.next.nextSibling)]
    # print postList[len(postList)-1]   #what if both dates on same page?
    postCount = len(postList) - postList.index(begin.next.nextSibling)
    end = siteHTML.findAll('h4', text=fromDate)
    repeatMax = 100  # option for max post page search
    while end == [] and repeatMax != 0:
        end, siteHTML = nextPage(siteHTML, baseUrl, fromDate)
        postCount = postCount + 100
        repeatMax = repeatMax - 1
    if end == False or repeatMax == 0:
      # print "couldn't find ending post"
      return "couldn't find ending post" + str(siteHTML)
    end = siteHTML.find('h4', text=fromDate)
    postList = siteHTML.findAll('p')
    del postList[len(postList) - 1]
    # print postList[0]
    # print postList[postList.index(end.previous.previous.previousSibling)]
    if str(end.previous.previous.previousSibling.name) == "table":
      postCount = postCount
    else:
      postCount = postCount + postList.index(end.previous.previous.previousSibling) + 1  # +1 for list
  else:
    postCount = postList.index(end.previous.previous.previousSibling) - postList.index(begin.next.nextSibling) + 1
  # print postCount
  return postCount

def topCount(url, city, top_category, fromDate, toDate):
    location_url = getLocationUrl(url, city)
    sub_categories_array = getLocationSubCate(location_url, top_category)
    sub_category_names, sub_categories_urls = sub_categories_array
    DBformatDate = convertTime(toDate)
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
    DBformatDate = convertTime(toDate)
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




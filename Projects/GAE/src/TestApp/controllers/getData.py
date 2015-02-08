import urllib2
import BeautifulSoup
import datetime
import time
import queryData
# import elinks

_DEBUG = True

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

def getPosts(self, baseUrl, dates):
  if len(dates[0]) == 0:
      return False
  baseUrl = baseUrl[:len(baseUrl) - 1]
  postTitles, postUrls, postId, postDate = [], [], [], []
  a = 0
  for url in range(0, len(self)):
    try:
      temp1 = str(self[url].a.string)
      postTitles.append(temp1)
      temp2 = str(self[url].a.get('href'))
      postUrls.append(baseUrl + temp2)
      temp3 = str(temp2)
      s = temp3.find("/") + 1
      s = temp3.find("/", s) + 1
      s = temp3.find("/", s) + 1
      e = temp3.find(".html", s)
      temp3 = temp3[s:e]
      postId.append(temp3)
    except:
      text = self[url].a.encode()
      s = text.find('href=') + 6
      e = text.find('"', s)
      link = text[s:e]
      postUrls.append(baseUrl + link)
      temp3 = link
      s2 = temp3.find("/")
      s2 = temp3.find("/", s2 + 1)
      e2 = temp3.find(".html", s2)
      temp3 = temp3[s2:e2]
      postId.append(temp3)
      s = text.find('>', e) + 1
      e = text.find('</a>', s)
      title = text[s:e]
      postTitles.append(title)
    try:
      if dates[1][a + 1] != postId[url]:  # assume first posting in page has date of first entry in
        postDate.append(dates[0][a])  # posting list. thus when postId equals the next date entry,
      else:  # new date is used until this condition occurs again
        postDate.append(dates[0][a + 1])
        a = a + 1
    except:
      postDate.append(dates[0][a])
  oldpostId = postId[:]
  repeatPosts = queryData.checkQueryPosts(oldpostId)
  if len(oldpostId) != 0 or len(oldpostId) != 1:
    if len(repeatPosts) != 0:
      if repeatPosts != False:
        cleanPosts = RemoveRepeatPosts(postTitles, postUrls, postId, postDate, repeatPosts)
        postTitles, postUrls, postId, postDate = cleanPosts
        return postTitles, postUrls, postId, postDate
  return postTitles, postUrls, postId, postDate

def gotoNextPage(self, baseUrl, EndDate):
    try:
        test = self.find('a', text='next 100 postings')
    except:
        return False
    footer = self.find('p', align='center')
    nextPageUrl = footer.findChild('a').get('href')
    HTML = urllib2.urlopen(baseUrl + nextPageUrl).read()
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    postDate_array = getPostDates(siteHTML, EndDate) 
    postList = siteHTML.findAll('p')
    del postList[len(postList) - 1]
    return_posts = getPosts(postList, baseUrl, postDate_array)
    if return_posts == False:
        return False
    postTitles, postUrls, postId, postDates = return_posts
    if len(postDates) == 0 or len(postDates) == 1:
        return False
    return postTitles, postUrls, postId, postDates, siteHTML

def getPostDates(self, EndDate):
  postDate = self.findAll('h4')
  postIdMark, postIdDate = [], []
  if len(postDate) != 1:
    for i in range(0, len(postDate)):
      z = str(postDate[i].nextSibling.nextSibling.a.get('href')).replace('.html', '')
      s = z.find('/') + 1
      s2 = z.find('/', s) + 1
      s3 = z.find('/', s2) + 1
      postIdMark.append(z[s3:])
      try:
        struct_time = time.strptime(postDate[i].string + " 2009", "%a %b %d %Y")
        cleanDate = time.strftime("%m%d%y", struct_time)
        if cleanDate == EndDate:
          return postIdDate, postIdMark
        postIdDate.append(cleanDate)
      except:
        postIdDate.append(cleanDate)
  else:
    struct_time = time.strptime(postDate[0].string + " 2009", "%a %b %d %Y")
    cleanDate = time.strftime("%m%d%y", struct_time)
    if cleanDate <= EndDate:
      return postIdDate, postIdMark
    else:
      postIdDate = list(cleanDate for i in range(0, 100))
      z = str(postDate[0].nextSibling.nextSibling.a.get('href')).replace('.html', '')
      s = z.find('/') + 1
      s2 = z.find('/', s) + 1
      s3 = z.find('/', s2) + 1
      postIdMark.append(z[s3:])
      return postIdDate, postIdMark
  return postIdDate, postIdMark

def getLastDate():
  today = datetime.date.today()
  difference = datetime.timedelta(days= -5)
  when = today + difference
  EndDate = when.strftime("%m%d%y")
  return EndDate

def checkDates(postDates, EndDate):
    lastDateEntry = 0
    for k in range(0, len(postDates)):
      if int(postDates[k]) <= EndDate:
        lastDateEntry = k
        break
    return lastDateEntry

def RemoveRepeatPosts(postTitles, postUrls, postId, postDate, repeatPosts):
    numDeleted = []
    for i in range(0, len(repeatPosts)):
        try:
            a = postId.index(repeatPosts[i])
            del postTitles[a]
            del postUrls[a]
            del postId[a]
            del postDate[a]
            numDeleted.append(1)
        except ValueError:
            pass
    # print len(numDeleted)
    return postTitles, postUrls, postId, postDate
    
    
#    for i in range(0,len(repeatPosts)):
#        a = postId.count(repeatPosts[i])
#        if a != 0:
#            del postTitles[a]
#            del postUrls[a]
#            del postId[a]
#            del postDate[a]
#            numDeleted.append(1)
#        elif a == 0:
#            postId.reverse()  #switched
#            a = postId.count(repeatPosts[i])
#            if a!= 0:
#                postId.reverse()  #normal
#                a = postId.count(repeatPosts[i])
#                del postTitles[a]
#                del postUrls[a]
#                del postId[a]
#                del postDate[a]
#                numDeleted.append(1)
#            else:
#                postId.reverse() #normal
#    return postTitles,postUrls,postId,postDate

def EvalPostPages(LocCateUrl, EndDate):
  HTML = urllib2.urlopen(LocCateUrl).read()
  siteHTML = BeautifulSoup.BeautifulSoup(HTML)
  postIdDate, postIdMark = getPostDates(siteHTML, EndDate)  # postDate_array = postIdDate,postIdMark
  postList = siteHTML.findAll('p')
  del postList[len(postList) - 1]
  postDate_array = postIdDate, postIdMark
  return_posts = getPosts(postList, LocCateUrl, postDate_array)
  if return_posts == False:
      return False
  postTitles, postUrls, postId, postDates = return_posts
  nextPostPage = gotoNextPage(siteHTML, LocCateUrl, EndDate)
  if nextPostPage is False:
      return postTitles, postUrls, postId, postDates
  while nextPostPage != False:  # and EndDate >= #last date of p:
    postTitles.extend(nextPostPage[0])
    postUrls.extend(nextPostPage[1])
    postId.extend(nextPostPage[2])
    postDates.extend(nextPostPage[3])
    siteHTML = nextPostPage[4]
    nextPostPage = gotoNextPage(siteHTML, LocCateUrl, EndDate)
    if nextPostPage is False:
      return postTitles, postUrls, postId, postDates
  else:
    return postTitles, postUrls, postId, postDates

def getLocations(url, city):
    try:
        line = "getLocations->"
        line = line + "getSiteUrls-"
        sites, siteUrls = getSiteUrls(url)
        line = line + "Loc_index-"
        Loc_index = sites.index(city)
        line = line + "Location_Name-"
        Location_Name = sites[Loc_index]
        line = line + "Location_Url-"
        Location_Url = siteUrls[Loc_index]
        return Location_Name, Location_Url
    except:
        return line

def getSub_Category(Location_Url, top_category, sub_category):
    categories, cateUrls = getLocationSubCate(Location_Url, top_category)
    Cate_index = categories.index(sub_category)
    Category_Name = categories[len(categories) - 1]  
    Category_Url = cateUrls[Cate_index]
    return Category_Name, Category_Url

def PostData(url, city, top_category, sub_category):
    line = "start-"
    Location_Name, Location_Url = getLocations(url, city)
    line = line + "second-"
    Category_Name, Category_Url = getSub_Category(Location_Url, top_category, sub_category)
    LocCateUrl = Location_Url + Category_Url
    line = line + "third-"
    EndDate = getLastDate()
    line = line + "fourth-"
    Loc_Cate_result = EvalPostPages(LocCateUrl, EndDate)
    line = line + "fifth-"
    postTitles, postUrls, postId, postDates = Loc_Cate_result
    return_result = Location_Name, Category_Name, postTitles, postUrls, postId, postDates
    return return_result

def test():
    url = "http://geo.craigslist.org/iso/us"
    city = "boston"
    top_category = "for sale"
    sub_category = "wanted"
    result = PostData(url, city, top_category, sub_category)
    return result

# print "start"
# print result
# testresult = test()
# print testresult[5][len(testresult[5])-1]
# print len(testresult)
# print postId
# print testresult[0]," - ",testresult[1]
# print testresult[2][0]," - ",testresult[3][0]," - ",testresult[4][0]," - ",testresult[5][0]

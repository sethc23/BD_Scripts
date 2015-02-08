import urllib2
import BeautifulSoup
import datetime
import time
import elinks
# import queryData



#
#
# if len(categText) == len(categUrls):
#    categories,subUrls = getCategories(subLinks)
#
#
# Category_Name,Category_Url = getSub_Category(Location_Url,top_category,sub_category)
# LocCateUrl = Location_Url+Category_Url
# line = line+"third-"
# EndDate = getLastDate()
# Loc_Cate_result = EvalPostPages(LocCateUrl,EndDate)
# line = line+"fourth-"
# postTitles,postUrls,postId,postDates = Loc_Cate_result
# return_result = Location_Name,Category_Name,postTitles,postUrls,postId,postDates

# print result



def getLocationSubCate(location, top_category):

  return categories, subUrls

def getCategories(self):

    return categText, categUrls

#####-------
#####-------
#####-------
#####-------

def getPosts(self, baseUrl, dates):
  baseUrl = baseUrl[:len(baseUrl) - 1]
  postTitles, postUrls, postId, postDate = [], [], [], []
  a = 0
  for url in range(0, len(dates[0])):
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
  print len(oldpostId)       
  # if len(postUrls) == len(postTitles):  #if information is expected and equal length
  # CleanPostId = queryData.checkQueryPosts(oldpostId)
    # if len(postId) != len(CleanPostId) and CleanPostId != False: 
        # cleanPosts = RemoveOldPosts(postTitles,postUrls,postId,postDate,CleanPostId)
        # return cleanPosts
    # else:
        # return False
  return postTitles, postUrls, postId, postDate

#####-------
#####-------
#####-------
#####-------

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
    postList.pop()
    postTitles, postUrls, postId, postDates = getPosts(postList, baseUrl, postDate_array)
    if len(postDates) == 0:
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

def RemoveOldPosts(postTitles, postUrls, postId, postDate, CleanPostId):
    CleanPostId.sort(reverse=True)
    a = len(postId) - 1
    while len(postId) != len(CleanPostId):
        try:
            b = CleanPostId.index(str(postId[a]))
            a = a - 1
        except:
            postTitles.pop(a)
            postUrls.pop(a)
            postId.pop(a)
            postDate.pop(a)
            a = len(postId) - 1
        if a == 0:
            break
    return postTitles, postUrls, postId, postDate

def EvalPostPages(LocCateUrl, EndDate):
  HTML = urllib2.urlopen(LocCateUrl).read()
  siteHTML = BeautifulSoup.BeautifulSoup(HTML)
  postIdDate, postIdMark = getPostDates(siteHTML, EndDate)  # postDate_array = postIdDate,postIdMark
  postList = siteHTML.findAll('p')
  postList.pop()
  postDates_array = postIdDate, postIdMark
  postTitles, postUrls, postId, postDates = getPosts(postList, LocCateUrl, postDates_array)
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
  return postTitles, postUrls, postId, postDates

def getLocations(url, city):

    return Location_Name, Location_Url

def getSub_Category(Location_Url, top_category, sub_category):
    categories, cateUrls = getLocationSubCate(Location_Url, top_category)
    Cate_index = categories.index(sub_category)
    Category_Name = categories[len(categories) - 1]  
    Category_Url = cateUrls[Cate_index]
    return Category_Name, Category_Url


url = "http://geo.craigslist.org/iso/us"
city = "boston"
top_category = "for sale"
sub_category = "wanted"
line = "start-"
result = urllib2.urlopen(url)
html = result.read()
links = BeautifulSoup.BeautifulSoup(html).findAll("a")
sites, siteUrls = [], []
for url in range(0, len(links)):
    try:
        temp1 = str(links[url].string)
        temp2 = str(links[url].get('href'))
        if temp1 == "None":
            temp1 = links[url].b.string
    except:
        x = str(links[url])
        print x
        z = str(x)
        s1 = z.find('href=') + 5
        e = z.find('"', s1)
        temp1 = z[s1:e]
        s2 = z.find('>', e) + 1
        e2 = z.find('>', s2)
        temp2 = z[s2:e2]
        
    sites.append(temp1)
    siteUrls.append(temp2)
    if temp2.find('www.craigs') == 7:
      sites.pop()
      siteUrls.pop()
    if temp2.find('forums.craigs') == 7:
      sites.pop()
      siteUrls.pop()
    if temp2.find('en.wikipedia') == 7:
      sites.pop()
      siteUrls.pop()


Loc_index = sites.index(city)
Location_Name = sites[Loc_index]
Location_Url = siteUrls[Loc_index]
HTML = urllib2.urlopen(Location_Url).read()
siteHTML = BeautifulSoup.BeautifulSoup(HTML)
subList = siteHTML.find('table', summary=top_category)
subLinks = subList.findChildren('a')
categText, categUrls = [], []
for url in range(0, len(subLinks)):
    temp1 = str(subLinks[url].string)
    categText.append(temp1)
    temp2 = str(subLinks[url].get('href'))
    categUrls.append(temp2)



# def test():


# result = test()
# print postId
# print testresult[0]," - ",testresult[1]
# print testresult[2][0]," - ",testresult[3][0]," - ",testresult[4][0]," - ",testresult[5][0]

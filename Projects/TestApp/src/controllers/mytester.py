import urllib2
import BeautifulSoup


####    success
####    first ad:  1053253447  on date:  Fri Feb 27

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


def getLocationSubCate(location, top_category):
  HTML = urllib2.urlopen(location).read()
  siteHTML = BeautifulSoup.BeautifulSoup(HTML)
  subList = siteHTML.find('table', summary=top_category)
  subLinks = subList.findChildren('a')
  categories, subUrls = getCategories(subLinks)
  return categories, subUrls

def getLastDate():
  today = datetime.date.today()
  difference = datetime.timedelta(days= -5)
  when = today + difference
  EndDate = when.strftime("%m%d%y")
  return EndDate


def getPostCount(startUrl, date):
    HTML = urllib2.urlopen(LocCateUrl).read()
    siteHTML = BeautifulSoup.BeautifulSoup(HTML)
    postDate_array = getPostDates(siteHTML, EndDate)
    # postIdDate,postIdMark = postDate_array
    postList = siteHTML.findAll('p')
    del postList[len(postList) - 1]
    
    return_posts = getPostsCount(postList, postDate_array)
    pass

def topCount(url, city, top_category, date):
    Location_Name, Location_Url = getLocations(url, city)
    sub_categories_array = getLocationSubCate(Location_Url, top_category)
    # #sub_category_names,sub_categories_urls = sub_categories_array
    return sub_categories_array[1][i], date, Location_Name, Location_Url
#    if len(sub_categories_array[0]) != len(sub_categories_array[1]):
#        return "sub_category_array mismatch"
#    for i in range(0,len(sub_categories_array[0])):
#        postCount.append(getPostCount(sub_categories_array[1][i],date))
#        postDate.append(date)
#    return postDate,sub_category_names,postCount

url = "http://geo.craigslist.org/iso/us"
city = "boston"
top_category = "for sale"
date = "Mon Mar 02"
result1 = postCount.topCount(url, city, top_category, date)
# date,sub_category,sub_count = result1

sub_categories_urls, date, Location_Name, Location_Url = result1

HTML = urllib2.urlopen(LocCateUrl).read()
siteHTML = BeautifulSoup.BeautifulSoup(HTML)
postDate_array = getPostDates(siteHTML, EndDate)
# postIdDate,postIdMark = postDate_array
postList = siteHTML.findAll('p')
del postList[len(postList) - 1]

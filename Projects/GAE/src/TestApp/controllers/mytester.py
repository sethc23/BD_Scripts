import urllib2
import BeautifulSoup
# import sendData
import getData

url = "http://geo.craigslist.org/iso/us"
result = getData.getData(url)
print "success"
print len(result[5])
# siteHTML = result


####    success
####    first ad:  1053253447  on date:  Fri Feb 27


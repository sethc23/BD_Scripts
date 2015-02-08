import urllib2, BeautifulSoup
import datetime, time
from queryData import sendHTML

_DEBUG = True

def saveWebPage(url):
    result = urllib2.urlopen(url)
    html = result.read()
    answer = sendHTML(html, url)
    if str(answer).find("success") == 0:
        return answer
    else:
        return "saveWebPageLinks error - " + answer

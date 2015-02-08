import urllib2
import urllib
data = {}
data['name'] = 'Somebody Here'
data['location'] = 'Northampton'
data['language'] = 'Python'
url_values = urllib.urlencode(data)
print url_values
# name=Somebody+Here&language=Python&location=Northampton
url = 'http://www.example.com/example.cgi'
full_url = url + '?' + url_values
data = urllib2.open(full_url)

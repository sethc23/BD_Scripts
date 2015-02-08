# -*- coding: utf-8 -*-
from mechanize import Browser
from datetime import datetime
from bs4 import BeautifulSoup

def getPageResults(beautiful_html, data, criteria):
    place_city = criteria
    h = beautiful_html
    page_results = h.find('div', {"class":"resultsListings"})
    item_results = page_results.findAll('div', {'class':'results-mod'})
    for item in item_results:
        nameDiv = item.find('p', {'class':'results-biz-name'})
        nameDiv = str(nameDiv.a.string).strip()
        numDiv = item.find('p', {'class':'bizPhone'})
        numDiv = str(numDiv.string).strip()
        addrDiv = item.find('span', {'class':'bizAddress'})
        addrDiv = str(addrDiv.string).strip()
        data.append(nameDiv + '	' + addrDiv[:addrDiv.lower().find(place_city.lower()) - 1] + '	' + addrDiv[addrDiv.lower().find(place_city.lower()):] + '	' + numDiv)
    return data

#------------Setup Browser
br = Browser()
br.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
br.set_handle_robots(False)

#------------WEBPAGE
# names,addresses,numbers = [],[],[]
data = []
queries = ['pediatric', 'schools']
cities = ['nashua', 'hudson', 'bedford', 'londonderry', 'amherst',
            'litchfield', 'hollis']
state = 'nh'

for query in queries:
    for place_city in cities:
        """
        query=
        place_city=
        """
        place_state = state
        page = '1'
        url = 'http://www.openlist.com/results/?query=' + query + '&place=' + place_city + ',+' + place_state + '&sort_by=name&page=' + page
        br.open(url)
        x = br.response().read()
        h = BeautifulSoup(x)
        if x.find('Showing 1 through 10 out of ') == -1:
            iterResults = '1'
        else:
            totalResults = x[x.find('Showing 1 through 10 out of ') + 28:x.find('.', x.find('Showing 1 through 10 out of ') + 28)]
            if totalResults[-1:] == '0':
                iterResults = eval(totalResults[:-1])
            else:
                iterResults = eval(totalResults[:-1]) + 1

        data = getPageResults(h, data, place_city)
        if iterResults != '1':
            for j in range(2, iterResults + 1):
                page = str(j)
                url = 'http://www.openlist.com/results/?query=' + query + '&place=' + place_city + ',+' + place_state + '&sort_by=name&page=' + page
                br.open(url)
                x = br.response().read()
                h = BeautifulSoup(x)
                data = getPageResults(h, data, place_city)

queries = ['pediatric', 'schools']
cities = ['westford', 'chelmsford']
state = 'ma'

for query in queries:
    for place_city in cities:  # query ==?  place_city ==?
        place_state = state
        page = '1'
        url = 'http://www.openlist.com/results/?query=' + query + '&place=' + place_city + ',+' + place_state + '&sort_by=name&page=' + page
        br.open(url)
        x = br.response().read()
        h = BeautifulSoup(x)
        totalResults = x[x.find('Showing 1 through 10 out of ') + 28:x.find('.', x.find('Showing 1 through 10 out of ') + 28)]
        if totalResults[-1:] == '0':
            iterResults = eval(totalResults[:-1])
        else:
            iterResults = eval(totalResults[:-1]) + 1

        data = getPageResults(h, data, place_city)

        for j in range(2, iterResults + 1):
            page = str(j)
            url = 'http://www.openlist.com/results/?query=' + query + '&place=' + place_city + ',+' + place_state + '&sort_by=name&page=' + page
            br.open(url)
            x = br.response().read()
            h = BeautifulSoup(x)
            data = getPageResults(h, data, place_city)
            
filepath = '/Users/admin/Desktop/output.txt'
f = open(filepath, 'a')
if f.readline(0) == '':
    header = 'NAME' + '	' + 'ADDRESS' + '	' + 'CITY/STATE/ZIP' + '	' + 'PHONE'
    f.write(header + '\n')
for line in data:
    f.write(line + '\n')
f.close()

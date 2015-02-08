import mechanize

br = mechanize.Browser()
url = 'http://s14.alluc.org/movies.html'
br.open(url)
links = []
for i in br.links():
    links.append(i.text)
br.close()
txt = str(links[:])
s = txt.find('(+')
b = txt.rfind("'", 0, s)
e = txt.find("'", b + 1)
start = txt[b + 1:e]
print start
s = txt.rfind('(+')
b = txt.rfind("'", 0, s)
e = txt.find("'", b + 1)
end = txt[b + 1:e]
print end
titles = links[links.index(start):links.index(end)]
print len(titles)

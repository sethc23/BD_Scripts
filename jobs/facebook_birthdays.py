from mechanize import Browser
from datetime import datetime

def getResults(x):
    s = x.find('<div class="abt acw">')
    s2 = x[:s].rfind('<div>')
    s = s2
    e = x.find('<div id="footer">')
    e2 = x[:e].rfind('</span>')
    e = x.find('</div>', e2)
    return x[s:e]

def getNames_Links(results):
    x = results
    name, url = [], []
    pt = 0
    for i in range(0, x.count('<div class="abt acw">')):
        s1 = x.find('<div class="ib"', pt)
        s = x.find('<a', s1)
        e = x.find('</a>', s)
        pt = e + 3
        row = x[s:e]
        s = row.find('href') + 6
        e1 = row.find('id', s)
        e = row.find('&', e1) + 1
        url.append(row[s:e].replace('amp;', ''))
        s = row.find('<span')
        s2 = row.find('>', s) + 1
        e = row.find('</span>', s2)
        name.append(row[s2:e].replace('&#039;', "'"))
    return name, url

def getLink_block(x):
    s = x.find('<span class="mfss fcg">')
    e = x.find('</span>', s) + len('</span>')
    link_block = x[s:e]
    return link_block

def getLink_urls(base_url, link_block):
    x = link_block
    url = []
    pt = 0
    for i in range(0, x.count('<a class="sec"')):
        s = x.find('<a', pt)
        e = x.find('</a>', s)
        pt = e + 3
        row = x[s:e]
        s = row.find('href') + 6
        e = row.find('"', s)
        url.append(base_url + row[s:e].replace('amp;', ''))
    return url

def getNewNames(base_url, link_list, ignore_names):
    names, urls = [], []
    old_links = []
    while link_list != []:
        gotoLink = link_list.pop(0)
        try:
            br.open(gotoLink)
        except:
            print gotoLink
            return
        start = gotoLink[gotoLink.find('start=') + len('start='):
                       gotoLink.find('&', gotoLink.find('start='))]
        end = gotoLink[gotoLink.find('end=') + len('end='):
                       gotoLink.find('&', gotoLink.find('end='))]
        list_range = start + '-' + end
        old_links.append(list_range)
        x = br.response().read()

        if x.find('>Showing:') == -1:
            link_block = getLink_block(x)
            new_links = getLink_urls(base_url, link_block)
            new_links.reverse()
            for item in new_links:
                start = item[item.find('start=') + len('start='):
                       item.find('&', item.find('start='))]
                end = item[item.find('end=') + len('end='):
                       item.find('&', item.find('end='))]
                list_range = start + '-' + end
                if old_links.count(list_range) == 0:
                    link_list.insert(0, item)
        results = getResults(x)
        new_names, new_links = getNames_Links(results)     
        for i in range(0, len(new_names)):
            if ignore_names.count(new_names[i]) == 0:
                if names.count(new_names[i]) == 0:
                    names.append(new_names[i])
                    urls.append(new_links[i])
    return names, urls

def getBdays(base_url, urls):
    bday = []
    for prof_link in urls:
        left = prof_link[:prof_link.find('fbb=')]
        right = prof_link[prof_link.find('fbb='):]
        new_link = left + 'v=info&' + right
        try:
            br.open(base_url + new_link)
        except:
            print base_url + new_link
            print urls.index(prof_link)
            return
        x = br.response().read()
        s = x.find('Birthday:</div>')
        if s == -1:
            bday.append('not listed')
        else:
            s2 = x.find('class="mfsm"', s) + len('class="mfsm"') + 1
            e2 = x.find('<', s2)
            date = x[s2:e2]
            if date.find(',') == -1:
                new_date = datetime.strptime(date, '%B %d')
            else:
                new_date = datetime.strptime(date, '%B %d, %Y')
            formatted_date = new_date.strftime('%m/%d/%y')
            bday.append(formatted_date)
    return bday

#------------Get Current List
f = open('/Users/admin/SERVER2/BD_Scripts/birthday_list.txt', 'r')
x = f.read()
f.close()
y = x.split('\r')
ignore_names, get_b_days = [], []
for pt in y:
    if pt.split('\t')[0] == 'x':
        ignore_names.append(pt.split('\t')[1])
    elif pt.split('\t')[0] == '-':
        get_b_days.append(pt.split('\t')[1])


#------------Setup Browser
br = Browser()
br.addheaders = [('user-agent', '   Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
br.set_handle_robots(False)

#------------LOGIN
startUrl = 'http://m.facebook.com/login.php?http&refsrc=http%3A%2F%2Fm.facebook.com%2F&no_next_msg&r5af71e39&refid=8'
br.open(startUrl)

br.select_form(nr=0)     
form = br.form
form.set_value("seth.t.chase@gmail.com", "email")
form.set_value("ferrarif50", "pass")
br.submit()  # submit current form


#------------get to "Everyone" page

# http://m.facebook.com/friends.php?a&fbb=r700a99ff&refid=5

for link in br.links(text='Profile'):
    br.follow_link(link)

for link in br.links(text='See More Posts'):
    x = link

base_url = x.base_url
base_url = base_url[:base_url.rfind('/')]  ####--####

txt = br.response().read()
pt = txt.find('See More Posts')
s = txt.find('>Friends (', pt) + 10
e = txt.find(')', s)
friend_count = eval(txt[s:e])  ####--####
iter_count = (friend_count // 10)

for link in br.links(text='Friends'):
    br.follow_link(link)  # 1

link_list = []
for link in br.links():
    if link.text.find('-') != -1:
        link_list.append(base_url + link.url)

names, urls = getNewNames(base_url, link_list, ignore_names)

bday = getBdays(base_url, urls)

new_names, new_bdays = [], []
updated_names, updated_bdays = [], []
for i in range(0, len(names)):
    if get_b_days.count(names[i]) != 0:
        if bday[i] != 'not listed':
            updated_names.append(names[i])
            updated_bdays.append(bday[i])
    elif get_b_days.count(names[i]) == 0:
        new_names.append(names[i])
        new_bdays.append(bday[i])


print 'Updates'
print ''
for j in range(0, len(updated_names)):
    print updated_bdays[j] + '	' + updated_names[j]

print ''
print '----------'
print ''
print 'New Names'
print ''
for j in range(0, len(new_names)):
    print new_bdays[j] + '	' + new_names[j]


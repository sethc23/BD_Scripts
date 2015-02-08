from appscript import *
from os import system, listdir
from time import sleep


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def activateSafari():
    app(u'Safari').activate()

def runScript(script):
    return app(u'Safari').documents[1].do_JavaScript(script)

def gotoUrl(url):
    activateSafari()
    orig_url = app(u'Safari').documents[1].URL.get()
    app(u'Safari').windows[1].tabs[1].properties.set({k.URL: url})
    if orig_url != url:
        checkLoaded(orig_url, url)

def getSource():
    activateSafari()
    x = app(u'Safari').windows[1].tabs[1].source.get()
    return x

def checkLoaded(orig_url, url):
    current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
    if current == url:
        next = True
    else:
        next = False
    if current == orig_url:
        stop, iter_num = False, 30
        while stop == False or iter_num != 0:
            sleep(2)
            current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
            if current == url:
                next = True
                stop = True
                break
            else:
                check = runScript('document.readyState')
                if check == 'complete':
                    return True
                else:
                    iter_num = iter_num - 1
        if iter_num == 0:
            return False
    current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')   
    if current == url or next == True:
        check = runScript('document.readyState')
        if check == 'complete':
            return True
        else:
            stop, iter_num = False, 60
            while stop == False or iter_num != 0:
                sleep(1)
                check = runScript('document.readyState')
                if check == 'complete':
                    return True
                else:
                    iter_num = iter_num - 1
            if iter_num == 0:
                return False

def getDataFromPage():
    activateSafari()
    workDir = '/Users/admin/Desktop'
    system('/usr/local/bin/cliclick c783 183')
    app(u'System Events').processes[u'Safari'].key_code(1)
    app(u'System Events').processes[u'Safari'].key_code(36)
    sleep(2)
    file_name = app(u'System Events').processes[u'Safari'].windows[1].sheets[1].text_fields[1].value.get()
    x_1 = listdir(workDir)
    if x_1.count(file_name.replace('/', ':') + '.webarchive') != 0:
        cmd = 'rm ' + workDir + '/' + file_name.replace(' ', '\ ').replace('/', ':') + '.webarchive'
        system(cmd)
        x_1 = listdir(workDir)
    app(u'System Events').processes[u'Safari'].windows[1].sheets[1].buttons[u'Save'].click()
    sleep(2)
    x = listdir(workDir)
    if len(x) == len(x_1):
        stop = False
        iter_num = 10
        while (stop == False or iter_num != 0):
            iter_num = iter_num - 1
            x = listdir(workDir)
            if len(x) == len(x_1) + 1:
                stop = True
                break
            else:
                sleep(1)
    url = workDir + '/' + file_name.replace('/', ':') + '.webarchive'
    gotoUrl('about:blank')
    gotoUrl(url)
    src = getSource()
    cmd = 'rm ' + workDir + '/' + file_name.replace(' ', '\ ').replace('/', ':') + '.webarchive'
    system(cmd)
    gotoUrl('about:blank')
    return src

def getTable(html, idVar):
    x = html
    s = x.find(idVar)
    s1 = x[:s].rfind("<table")
    e = x.find("</table>", s) + len("</table>")
    return x[s1:e]

def getTags(text, tag):
    if type(text) == list:
        x = ''
        for it in text:
            x = x + it
        text = x
    tagList = []
    pt = 0
    for i in range(0, text.count('<' + tag)):
        s = text.find('<' + tag, pt)
        s1 = text.find('>', s) + 1
        e = text.find('</' + tag + '>', s)
        pt = e + len('</' + tag + '>')
        tagList.append(text[s1:e])
    return tagList

def cleanNumVar(x):
    abbr = ['T', 'M', 'B']
    for i in range(0, len(abbr)):
        if x.count(abbr[i]) != 0:
            s = x.find('.') + 1
            e = x.find(abbr[i])
            end = len(x[s:e])
            decimalCount = ((i + 1) * 3) - end
            x = x.replace('.', '').replace(abbr[i], '')
            for j in range(0, decimalCount):
                x = x + '0'
            return x
    return x


url = 'http://www.google.com/finance/stockscreener#c0=MarketCap&c1=PE&c2=Price52WeekPercChange&c3=High52Week&c4=QuoteLast&c5=Low52Week&c6=QuotePercChange&min6=1&max6=5&c7=Price13WeekPercChange&min7=2.14&c8=Price26WeekPercChange&region=us&sector=AllSectors&sort=&sortOrder='

gotoUrl('about:blank')

gotoUrl(url)
sleep(2)
html = getDataFromPage()

table = getTable(html, 'class="advanced_search_results results innermargin gf-table"')
table = getTags(table, 'tbody')[0]

tableRows = getTags(table, 'tr')
headerLabels = getTags(tableRows[0], 'b')
tableRows = tableRows[1:]

data = []
data.append(headerLabels)

s = html.find('class="tpsd"')
s1 = html.find('of', s) + 3
e = html.find(' rows', s1)
rowCount = eval(html[s1:e])

iterCount = (rowCount // 20)
if str(rowCount / 20.0)[str(rowCount / 20.0).find('.') + 1:] != '0':
    iterCount = iterCount + 1

#-----


def processTable(html, table, data):
    x, dataRows = html, table           
    dataRows = getTags(table, 'tr')
    for i in range(0, 20):
        it = dataRows[i]
        rowVars = getTags(it, 'td')
        tempVars = []
        for pt in rowVars[:-1]:
            if pt.find('</a>') != -1:
                x = getTags(pt, 'a')
                pt = x[:]
            if pt[0].isdigit():
                pt = cleanNumVar(pt)
                pt = eval(pt)
            if type(pt) == list:
                pt = pt[0]
            tempVars.append(pt)
        data.append(tempVars)

    s = table.find('class="SP_arrow_next"')
    s1 = table[:s].rfind('<a href="') + len('<a href="')
    e = table.find('"', s1)
    nextPage = 'http://www.google.com' + table[s1:e]
    nextPage = nextPage.replace('amp;', '')
    print nextPage
    return data, nextPage


#-----

for i in range(0, iterCount):
    data, nextPage = processTable(html, table, data)
    if i != iterCount - 1:
        gotoUrl(nextPage)
        sleep(2)
        html = getDataFromPage()
        table = getTable(x, 'class="advanced_search_results results innermargin gf-table"')
        table = getTag(table, 'tbody')


print rowCount
print len(data)



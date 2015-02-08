#!/usr/bin/env python

from appscript import app
from time import sleep
from bs4 import BeautifulSoup
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import click
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from HTML_API import getAllTag

def activate():
    app(u'Safari').activate()
    sleep(.3)
    x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
    end = 3 * 60
    while x != 'complete':
        sleep(.3)
        x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
        # print x
        end = end - 1
        if end == 0: break

def openUrl(url):
    activate()
    app(u'Safari').documents[1].URL.set(url)
    sleep(.3)
    x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
    end = 3 * 60
    while x != 'complete':
        sleep(.3)
        x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
        # print x
        end = end - 1
        if end == 0: break

def SaveAsPDF(fileSaveName):
    app(u'Safari').activate()
    app(u'System Events').processes[u'Safari'].menu_bars[1].menu_bar_items[u'File'].menus[1].menu_items[u'Print\u2026'].click()
    sleep(.3)
    app(u'System Events').processes[u'Safari'].windows[1].sheets[1].menu_buttons[u'PDF'].click()
    sleep(.3)
    app(u'System Events').processes[u'Safari'].windows[1].sheets[1].menu_buttons[u'PDF'].menus[1].menu_items[u'Save as PDF\u2026'].click()
    sleep(.3)
    app(u'System Events').processes[u'Safari'].windows[u'Save'].text_fields[1].select()
    
    app(u'System Events').processes[u'Safari'].keystroke(fileSaveName)
    app(u'System Events').processes[u'Safari'].windows[u'Save'].buttons[u'Save'].click()

def printToDefault():
    app(u'Safari').activate()
    x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
    if x == 'complete': app(u'Safari').documents[1].print_(print_dialog=False)
    end = 120 * 3
    while x != 'complete':
        sleep(.3)
        x = app(u'Safari').do_JavaScript(u'document.readyState', in_=app.documents[1])
        end = end - 1
        if end == 0:
            print 'failed'
            print asdas
            break    

def runScript(script):
    activate()
    return app(u'Safari').windows[1].tabs[1].do_JavaScript(script)

def goBack():
    app(u'Safari').activate()
    sleep(.5)
    app(u'System Events').application_processes[u'Safari'].key_code(33, using=k.command_down)

def goForward():
    app(u'Safari').activate()
    app(u'System Events').application_processes[u'Safari'].key_code(30, using=k.command_down)
    

def gotoUrl(url):
    activate()
    orig_url = app(u'Safari').documents[1].URL.get()
    app(u'Safari').windows[1].tabs[1].properties.set({k.URL: url})
    checkLoaded(orig_url, url)

def getUrl():
    return runScript('document.URL')

def getSource():
    activate()
    x = runScript("document.getElementsByTagName('html')[0].innerHTML")
    # x=app(u'Safari').windows[1].tabs[1].source.get()
    # if len(x) == 0:    
    return x

def saveHTML(savePath, findStr=['tag', 'attr', 'attr_value']):  # attr={'id' : 'id_value'}
    x = getSource()
    if len(x) == 0:
        print 'no source!'
        print asd
    soup = BeautifulSoup(x)
    if findStr != ['tag', 'attr', 'attr_value']:
        if len(findStr) == 3:
            a = soup(findStr[0], recursive=True, attrs={findStr[1] : findStr[2]})
            b, d = '', ''
            b = [str(c) for c in a[0].contents]
            for i in range(0, len(b)): d += b[i]
        if len(findStr) == 1:
            d = soup.tbody
            print str(d)
    f = open(savePath, 'w')
    f.write(d)
    f.close()

def saveHTMLpage(saveDir):
    click('716 443 c758 326')
    app(u'System Events').processes[u'Safari'].key_code(1)
    app(u'System Events').processes[u'Safari'].key_code(36)
    sleep(2)
    file_name = app(u'System Events').processes[u'Safari'].windows[1].sheets[1].text_fields[1].value.get()
    x_1 = listdir(saveDir)
    app(u'System Events').processes[u'Safari'].windows[1].sheets[1].buttons[u'Save'].click()
    sleep(2)
    x = listdir(saveDir)
    if len(x) == len(x_1):
        stop = False
        iter_num = 10
        while (stop == False or iter_num != 0):
            iter_num = iter_num - 1
            x = listdir(saveDir)
            if len(x) == len(x_1) + 1:
                stop = True
                break
            else:
                sleep(1)

def checkLoaded(orig_url, url=''):
    sleep(2)
    check_url = getUrl()
    if check_url != orig_url: url = check_url
    print 'url=\n', url, '\n'
    if url != '':
        current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
        if current == url:
            next = True
        else:
            next = False
        if current == orig_url:
            stop, iter_num = False, 60
            while stop == False or iter_num != 0:
                sleep(1)
                current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
                if current == url:
                    next = True
                    stop = True
                    break
                else:
                    iter_num = iter_num - 1
            if iter_num == 0:
                return False
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
    else:
        sleep(5)
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

#------
def getPagesFromTextLinks(text):
    x = text
    link_list = []
    pt = 0
    for i in range(0, x.count('target=')):
        s = x[:x.find('target=', pt) - 5].rfind('"') + 1
        e = x.find('"', s + 5)
        pt = x.find('</tr>', e)
        link_list.append(x[s:e].replace('amp;', ''))

    activateSafari()
    for i in range(0, len(link_list)):
        gotoUrl(link_list[i])
        system('/usr/local/bin/cliclick 716 443 c758 326')
        app(u'System Events').processes[u'Safari'].key_code(1)
        app(u'System Events').processes[u'Safari'].key_code(36)
        sleep(2)
        file_name = app(u'System Events').processes[u'Safari'].windows[1].sheets[1].text_fields[1].value.get()
        x_1 = listdir('/Users/admin/Desktop/McCarthy_on_TM')
        app(u'System Events').processes[u'Safari'].windows[1].sheets[1].buttons[u'Save'].click()
        sleep(2)
        x = listdir('/Users/admin/Desktop/McCarthy_on_TM')
        if len(x) == len(x_1):
            stop = False
            iter_num = 10
            while (stop == False or iter_num != 0):
                iter_num = iter_num - 1
                x = listdir('/Users/admin/Desktop/McCarthy_on_TM')
                if len(x) == len(x_1) + 1:
                    stop = True
                    break
                else:
                    sleep(1)

def expand_current_TOC(x):
    soup = BeautifulSoup(x)
    a = soup("table", id="tocContentTbl")
    b = str(a[0].contents)
    c = BeautifulSoup(b)
    d = c('tr')
    expand_links = []
    for it in d:
        if str(it.attrs) != "[]":
            e = it("td")
            for col in e:
                if str(col(attrs={'alt' : 'Expand'})) != "[]":
                    expand_links.append(col.a.get('href'))
    for it in expand_links:
        runScript(it)


def MakeEbook():
    f = open('/Users/admin/Desktop/ebook_links.html', 'r')
    x = f.read()
    f.close()
    
    links, pt = [], 0
    for i in range(0, x.count('href')):
        s = x.find('href', pt) + 6
        e = x.find('"', s)
        pt = e + 1
        if x[s:e].find('#') == -1:
            if links.count(x[s:e]) == 0: 
                links.append(x[s:e])
    
    baseUrl = 'file:////Users/admin/Library/Application Support/Firefox/Profiles/nvoog4xy.default/epub/21/'
    pt2 = 1
    for i in range(0, len(links)):
        it = baseUrl + links[i]
        openUrl(it)
        printToDefault()
        # SaveAsPDF('evidence'+str(i))

#MakeEbook()

"""

should add section to:
open first printed pdf, insert all remaining pages of pdf, save PDF with new name, delete old files
"""

import os
from sys import path
path.append(os.path.join(os.environ['BD'],'files_folders'))
from API_system import getClipboardData
from appscript import *
from time import sleep
from bs4 import BeautifulSoup

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def activate():
    app(u'Google Chrome').activate()

def openUrl(url):
    activate()
    gotoUrl(url)

def runScript(script):
    activate()
    x = app(u'Google Chrome').windows[1].tabs[1].execute(javascript=script)
    checkLoaded('', '')
    return x

def gotoUrl(url):
    app(u'Google Chrome').windows[1].tabs[1].properties.set({k.URL: url})

def getSource():
    # app(u'Google Chrome').activate()
    '''
    app(u'Google Chrome').windows[1].tabs[1].view_source()
    sleep(2)
    z=app(u'Google Chrome').windows[1].tabs[1].loading()
    while z == "True":
        sleep(1)
        z=app(u'Google Chrome').windows[1].tabs[1].loading()
    app(u'Google Chrome').windows[1].tabs[2].select_all()
    sleep(1)
    app(u'Google Chrome').windows[1].tabs[2].copy_selection()
    sleep(1)
    x=getClipboardData()
    sleep(1)
    app(u'Google Chrome').windows[1].tabs[2].close()
    return x
    '''
    a = "document.getElementsByTagName('html')[0].innerHTML"
    return runScript(a)

def goBack():
    app(u'Google Chrome').activate()
    sleep(.5)
    app(u'System Events').application_processes[u'Google Chrome'].key_code(33, using=k.command_down)
# app(u'System Events').application_processes[u'Acrobat'].key_code(120, using=k.control_down)

def goForward():
    app(u'Google Chrome').activate()
    app(u'System Events').application_processes[u'Google Chrome'].key_code(30, using=k.command_down)

def getUrl():
    return runScript('document.URL')

def saveHTML(savePath, findStr='html'):  # attr={'id' : 'id_value'}
    x = getSource()
    soup = BeautifulSoup(x)
    a = soup('div', recursive=True, attrs={'id' : 'bodystyle'})
    b, d = '', ''
    b = [str(c) for c in a[0].contents]
    for i in range(0, len(b)): d += b[i]
    f = open(savePath, 'w')
    f.write(d)
    f.close()

def checkLoaded(a,b):
    sleep(4)
    x = app(u'Google Chrome').windows[1].tabs[1].loading()
    z = str(app(u'Google Chrome').windows[1].tabs[1].execute(javascript="document.readyState;"))
    while z != "complete" or x == True:
        sleep(5)
        z = str(app(u'Google Chrome').windows[1].tabs[1].execute(javascript="document.readyState;"))
        x = app(u'Google Chrome').windows[1].tabs[1].loading()
    return
    """
    before submit, get url
    
    url=app(u'Safari').documents[1].URL.get()
    
    if url still same, wait
    if url different, then do readystate check
    repeat until ...
        checkLoaded='document.readyState'
    end repeat
    """

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
        checkLoaded()


'''
x=getSource()
pt=0
while x.find('alt="Expand"') != -1:
    pt+=1
    print pt
    expand_current_TOC(x)
    x=getSource()
'''

# print x
# runScript("javascript:pToc.opnNd('TAAB',1,'1')")



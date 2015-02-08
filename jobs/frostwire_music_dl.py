from appscript import *
from time import sleep, time

def newSearch():
    app(u'FrostWire').activate()
    sleep(.5)
    app(u'System Events').processes[u'FrostWire'].windows[u'FrostWire: Share it with your friends'].tab_groups[1].splitter_groups[1].buttons[u'Back To Search'].click()
    sleep(2)
    app(u'System Events').processes[u'FrostWire'].keystroke(title)
    sleep(2)
    # tab key
    app(u'System Events').processes[u'FrostWire'].key_code(48)
    app(u'System Events').processes[u'FrostWire'].keystroke(artist)
    sleep(2)
    # enter key
    app(u'System Events').processes[u'FrostWire'].key_code(36)
    sleep(3)

def waitForResults():
    now = int(time())
    min3ahead = int(time()) + (60)
    try:
        numResults = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].count(each=k.UI_element)
    except:
        sleep(10)
        numResults = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].count(each=k.UI_element)
    if numResults == 0:
        stop = False
        while stop == False:
            try:
                numResults = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].count(each=k.UI_element)
            except:
                pass
            if numResults != 0:
                stop = True
                break
            if min3ahead <= now:
                stop = True
                break
        now = int(time())
        min3ahead = int(time()) + (60)
    stop = False
    var = False
    while stop == False:
        if min3ahead <= now:
            var = False
            return var
            stop = True
        numPpl, name, size = getResultInfo(1)
        size = str(size).replace('KB', '').replace(',', '').strip()
        if (name.lower().replace(',', '').replace("'", '').find(artist.lower()) != -1
            and name.lower().replace(',', '').replace("'", '').find(title.lower()) != -1):
            if eval(str(numPpl)) >= 2:
                if eval(str(size)) > 1500:
                    var = True
                    return var
                    stop = True
    return var


def getResultInfo(num):
    if num == "":
        num = 1
    app(u'FrostWire').activate()
    try:
        numPpl = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[2 + ((num - 1) * 9)].value.get()
    except:
        numPpl = 1 
    name = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[5 + ((num - 1) * 9)].value.get()
    size = app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[7 + ((num - 1) * 9)].value.get()
    return numPpl, name, size

def verifyResult(info, title, artist):
    numPpl, name, size = info
    size = str(size).replace('KB', '').replace(',', '').strip()
    if size.lower().find('mb') != -1:
        return False
    if (name.lower().replace(',', '').replace("'", '').find(artist.lower()) != -1
        and name.lower().replace(',', '').replace("'", '').find(title.lower()) != -1):
        if eval(str(numPpl)) >= 2:
            if eval(str(size)) > 1500:
                return True
    return False

def nextResult():
    app(u'FrostWire').activate()
    # down key
    sleep(.25)
    app(u'System Events').processes[u'FrostWire'].key_code(125)
    sleep(.25)
    return

def downloadResult():
    app(u'FrostWire').activate()
    sleep(.25)
    app(u'System Events').processes[u'FrostWire'].windows[u'FrostWire: Share it with your friends'].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].buttons[u'Download'].click()
    sleep(.25)
    return

def startTopResult():
    sleep(.25)
    for i in range(0, 3):
        app(u'System Events').processes[u'FrostWire'].key_code(48)
        sleep(.10)
    for i in range(0, 6):
        app(u'System Events').processes[u'FrostWire'].key_code(116)
        sleep(.10)

"""
get info from text file


"""

f = open('/Users/admin/Desktop/music_list.txt', 'r')
x = f.read()
f.close()

y = x.split('\r')

noResultList = []

for item in y:
    # item=y[0]
    title = item[item.find(' - ') + 3:]
    artist = item[:item.find(' - ')]
    # print title
    # print ''
    # print artist
    newSearch()
    raw_input('?')
'''
    ready = waitForResults()
    #print 'ready',ready
    if ready == False:
        noResultList.append(item+'\r')
    else:
        startTopResult()
        info = getResultInfo(1)
        if verifyResult(info,title,artist) != True:
            gdResult=False
            for i in range(2,12):
                nextResult()
                info = getResultInfo(i)
                if verifyResult(info,title,artist) == True:
                    gdResult=True
                    break
            if gdResult == True:
                downloadResult()
                sleep(1)
            else:
                noResultList.append(item+'\r')

        else:
            downloadResult()
            sleep(1)


    

            

f=open('/Users/admin/Desktop/music_list_notFound.txt','w')
for item in noResultList:
    f.write(item)
f.close()
'''

'''
app(u'FrostWire').activate()

#number of downloaders
app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[2].value.get()

#name
app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[5].value.get()

#size
app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].static_texts[7].value.get()

#click back to search button
app(u'System Events').processes[u'FrostWire'].windows[u'FrostWire: Share it with your friends'].tab_groups[1].splitter_groups[1].buttons[u'Back To Search'].click()

#click download button
app(u'System Events').processes[u'FrostWire'].windows[u'FrostWire: Share it with your friends'].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].buttons[u'Download'].click()

#number of search results
app(u'System Events').processes[u'FrostWire'].windows[1].tab_groups[1].splitter_groups[1].splitter_groups[1].tab_groups[1].scroll_areas[1].tables[1].count(each=k.UI_element)

#tab key
app(u'System Events').processes[u'FrostWire'].key_code(48)

#keystroke string
app(u'System Events').processes[u'FrostWire'].keystroke(u'STRING')

#enter key
app(u'System Events').processes[u'FrostWire'].key_code(36)

#down key
app(u'System Events').processes[u'FrostWire'].key_code(125)
'''

# #back to search, title, tab, artist, enter
# #wait for enough results -- top one must have at least 4 --
        # #if 3 min goes by and no luck, print out title and move on
        # #if within time enough results come up
            # click download
            

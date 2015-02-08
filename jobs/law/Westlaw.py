from appscript import *
from os import system, listdir
from time import sleep
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from Safari_API import checkLoaded, getSource, gotoUrl, runScript

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def openWestlaw():
    app(u'Safari').activate()
    app(u'Safari').windows[1].tabs[1].properties.set({k.URL: u'http://www.westlaw.com'})

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
    for i in range(1176, len(link_list)):
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

def removeLinks(new_doc):
    x = new_doc
    pt = 0
    links = []
    for i in range(0, x.count('a href=')):
        s = x.find('<a href=', pt)
        e = x.find('>', s) + 1
        pt = e
        links.append(x[s:e])
    links.append('</a>')
    for item in links:
        x = x.replace(item, '')
    return x

def clean_McCarthy(text):
    x = text
    header = '<html>' + x[x.find('<head>'):x.find('</head>') + 7] + '<body>'

    # start of document
    pt = x.find('class="DocumentBody"')
    pt2 = x[:pt].rfind('<span')
    s = x.find('<strong>', pt2)
    x = x[s:]

    # end of document
    e = x.find('END OF DOCUMENT')
    s = x[:e].rfind('<div>')
    x = x[:s]

    footer = '</body></html>'

    new_doc = header + x + footer

    x = new_doc.find("West's Key Number Digest")
    if x != -1:
        s = new_doc[:x].rfind('<strong>')
        pt = new_doc.rfind('Key Number')
        e = new_doc.find('<br><br>', pt) + 8
        new_doc = new_doc[:s] + new_doc[e:]

    del_list = [('<br><br><br><br><br>', '')]


    for old, new in del_list:
        new_doc = new_doc.replace(old, new)

    new_doc = removeLinks(new_doc)        

    return new_doc

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def loginWestlaw():
    script = "document.getElementById('OnePassHeaderLink').text;"
    test = runScript(script)
    if test != "Switch to Westlaw Password Sign On":
        script = ("document.getElementById('OnePassHeaderLink').href;")
        link = runScript(script)
        gotoUrl(link)
    script = ("document.forms['mysignon'].elements['myname'].value='sthomas23';" + 
            "document.forms['mysignon'].elements['mypwd'].value='F*rrari1';" + 
            "document.forms['mysignon'].elements['myclientid'].value='sthomas23';" + 
            "document.forms['mysignon'].submit();")
    runScript(script)

def getSourceOfTOC():
    script = ("x=document.getElementsByTagName('frame')[1];" + 
        "a=x.contentDocument;" + 
        "b=a.body.getElementsByTagName('form')['formControl'];" + 
        "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];" + 
        "c.innerHTML;")
    script = ("x=document.getElementById('tocContentTbl');")
    return runScript(script)

#--------------------------------------------------------------------------------------
#--STEP 1------------------------------------------------------------------------------

# openWestlaw()
# loginWestlaw()

#--STEP 2------------------------------------------------------------------------------

# f=open('/Users/admin/Desktop/source.html','r')
# x=f.read()
# f.close()
# x=getSourceOfTOC()
# print x


# get links from text document, goto each url, save page as webarchive
# f=open('/Users/admin/Desktop/McCarthy Links.txt','r')
# x=f.read()
# f.close()
# getPagesFromTextLinks(x)

#--STEP 3------------------------------------------------------------------------------

# work_dir='/Users/admin/Desktop/McCarthy_on_TM/web_archives'
# new_dir='/Users/admin/Desktop/McCarthy_on_TM/htmls'
# x=listdir(work_dir)
# x.pop(x.index('.DS_Store'))
'''
y=listdir(new_dir)
y.pop(y.index('.DS_Store'))
z=[]
for i in range(0,len(x)):
    if y.count(x[i].replace('.webarchive','.html')) == 0:
        z.append(x[i])
'''
'''
for i in range(0,len(x)):
    item=x[i]
    url='file://'+work_dir+'/'+item
    gotoUrl(url)
    src=getSource()
    src2=src.encode('ascii','ignore')
    new_doc=clean_McCarthy(src2)
    new_name=item.replace('.webarchive','.html')
    f=open(new_dir+'/'+new_name,'w')
    f.write(new_doc)
    f.close()
'''



'''
script=("x=document.getElementsByTagName('frame')[1];"+
    "a=x.contentDocument;"+
    "c=b.firstChild"+
    "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];"+
    "c.innerHTML;")

script = (
     'function clickExpandLinks(source){'+
     "var links = source.getElementsByTagName('a');"+
     'var linkCount = links.length;'+
     'for (var i = 0; i < linkCount; i++)'+
         'url = links[i].href'+
         "if (url.search('action=ExpandTree')!=1 {"+
            
             '}'+
     'return wordList;'+ 
     '}'+
     'clickExpandLinks(source);')
'''

f = open('/Users')


# print runScript(script)
'''
<a href="javascript:void(pToc.tc2dc('TAABAABAABAAB','54MF-5DK0-00SR-P0R5-00000-00','','','1'));" target="_self" name="TAABAABAABAAB" onclick="return chClr(this);"><span id="hdr_TAABAABAABAAB">§ 1.1-</span> Introduction</a>

<a href="javascript:pToc.opnNd('TAAB',1,'1')" target="_self"><img src="/ri/IconShow.gif" width="12" height="12" alt="Expand" border="0" title="" align="bottom" onclick="ihd();" onmouseover="sd('TAAB', this);" onmouseout="dhd();" style="padding-top:2px"></a>

<a href="javascript:pToc.clsNd('TAAB',1,'1')" target="_self"><img src="/ri/IconHide.gif" width="12" height="12" alt="Collapse" border="0" title="" align="bottom" onclick="ihd();" onmouseover="sd('TAAB', this);" onmouseout="dhd();" style="padding-top:2px"></a>
'''
# all links with action=ExpandTree

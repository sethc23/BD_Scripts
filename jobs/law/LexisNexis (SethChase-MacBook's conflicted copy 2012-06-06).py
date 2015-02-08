from appscript import *
from bs4 import BeautifulSoup
from os import system, listdir
from time import sleep
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from Chrome_API import activate, runScript, gotoUrl, goBack, getUrl, checkLoaded, getSource
from Chrome_API import expand_current_TOC, saveHTML
# from Safari_API import activate,runScript,gotoUrl,goBack,getUrl,checkLoaded,getSource
# from Safari_API import expand_current_TOC, saveHTML
from API_system import click, getFilesFolders
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def chr_openLexis():
    activate()
    app(u'Google Chrome').windows[1].tabs[1].properties.set({k.URL: u'http://www.lexisnexis.com/lawschool/login.aspx'})

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

def loginLexis():
    activate()
    # script="document.getElementById('OnePassHeaderLink').text;"
    # test=runScript(script)
    # if test != "Switch to Westlaw Password Sign On":
    #    script=("document.getElementById('OnePassHeaderLink').href;")
    #    link=runScript(script)
    #    gotoUrl(link)
    script = ("document.forms['form1'].elements['txtLoginID'].value='sthomas23';" + 
            "document.forms['form1'].elements['txtPassword'].value='ferrari1';" + 
            "document.forms['form1'].elements['cmdSignOn'].click();")
    runScript(script)

def Navigate1():
    activate()
    script = ("x=document.getElementsByTagName('frame')[1];" + 
        "a=x.contentDocument;" + 
        "b=a.body.getElementsByTagName('form')['formControl'];" + 
        "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];" + 
        "c.innerHTML;")
    return runScript(script)

def getSourceOfTOC():
    activate()
    script = ("x=document.getElementsByTagName('frame')[1];" + 
        "a=x.contentDocument;" + 
        "b=a.body.getElementsByTagName('form')['formControl'];" + 
        "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];" + 
        "c.innerHTML;")
    script = ("x=document.getElementsByTagName('frame')[1];" + 
        "a=x.contentDocument;" + 
        "b=a.body.getElementsByTagName('form')['formControl'];" + 
        "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];" + 
        "c.innerHTML;")
    script = ("x=document.getElementById('tocContentTbl');")
    return runScript(script)

def getIndexExpandLinks():
    x = getSource()
    soup = BeautifulSoup(x)
    a = soup("table", id="tocContentTbl")
    b = str(a[0].contents)
    c = BeautifulSoup(b)
    d = c('tr')
    expand_links, parentID_list = [], []
    for i in range(28, len(d)):
        print i
        it = d[i]
        parentType, parentID = it.name, it.get('id')
        if str(it.attrs) != "[]":
            e = it("td")
            for col in e:
                if str(col(attrs={'alt' : 'Expand'})) != "[]":
                    expand_link = col.a.get('href')
                    runScript(expand_link)
                    checkLoaded(expand_link, '')
                    expandTreeLinks(parentType, parentID, expand_link)
    return expand_links

def expandTreeLinks(parentType, parentID, expand_link):
    # get saved files
    saveDirList = getFilesFolders('/Users/admin/Desktop/print')
    excludeList = []
    for it in saveDirList: excludeList.append(it.rstrip('.txt'))
    
    x = getSource()
    soup = BeautifulSoup(x)
    table = soup("table", id="tocContentTbl")
    b = str(table[0].contents)
    c = BeautifulSoup(b)
    tableTrees = c('tr')
    # expand_links,parentID_list=[],[]
    for row in tableTrees:
        if str(row.attrs) == "[]": 
            # when a link is in the tree
            a = getTOCchildren(parentID, c)
            for link in a:
                # print link
                linkID = link[link.find("'") + 1:link.find("'", link.find("'") + 1)]
                if excludeList.count(linkID) != 0: pass
                else:       
                    runScript(link)
                    url = getUrl
                    checkLoaded(url, '')
                    findStr = "'div',attr={'div' : 'bodystyle'}"
                    savePath = '/Users/admin/Desktop/print/' + linkID + '.txt'
                    saveHTML(savePath, findStr)
                    url = getUrl
                    goBack()
                    checkLoaded(url, '')
                    # break
            # print 'Close Tree'
            a = soup("tr", id=parentID)
            for row in a: 
                if str(row(attrs={'alt' : 'Collapse'})) != "[]":
                    closeTree = row.a.get('href')
                    runScript(closeTree)
            return 'done'
        else:
            #  execute when no links to download in tree?
            if it.name != parentID and str(it.name).find(parentID) != -1:
                e = it("td")
                for col in e:
                    if str(col(attrs={'alt' : 'Expand'})) != "[]":
                        expand_link = col.a.get('href')
                        runScript(expand_link)
                        checkLoaded(expand_link, '')

'''
rows_opened=[]
for i in range(0,len(treeRows)):
	open row
	rows_opened.append(row)
	check_loaded
	define boundaries of new rows
	add all new rows in boundaries to process List
	while process_list != 0:
		for all things in processList:
			if page, download
			if expand, add to tempList
		if tempList != []:
			tempList.reverse()
			for it in tempList: process_list.insert(0,it)
			x=process_list.pop(0)
			open x
			check_loaded
			rows_opened.append(x)
		else:
			close x
			if len(process_list) != 0:
				x=process_list.pop(0)
				open x
				check_loaded
				rows_opened.append(x)
'''                

def getTOCchildren(parent, source):
    x = parent
    y = 'abcdefghijklmnopqrstuvwxyz'
    y = y.upper()
    child_list = []
    for i in range(0, len(y)):
        for j in range(0, len(y)):
            for k in range(1, len(y)):
                child = y[i] + y[j] + y[k]
                newID = parent + child
                a = source("tr", id=newID)
                if len(a) == 0: return child_list
                b = BeautifulSoup(str(a[0].contents))
                c = b("a", onclick="return chClr(this);")
                newUrl = c[0].get('href')
                child_list.append(newUrl)

def getPagesFromTextLinks(text):
    x = text
    link_list = []
    pt = 0
    for i in range(0, x.count('target=')):
        s = x[:x.find('target=', pt) - 5].rfind('"') + 1
        e = x.find('"', s + 5)
        pt = x.find('</tr>', e)
        link_list.append(x[s:e].replace('amp;', ''))
    activate()
    for i in range(0, len(link_list)):
        gotoUrl(link_list[i])
        attr = {'div' : 'bodystyle'}
        saveHTML('/Users/admin/Desktop/print', attr)


# <a href="javascript:void(pToc.tc2dc('TAABAAB','55HS-RKP0-00YP-9002-00000-00','','','1'));" target="_self" #name="TAABAAB" onclick="return chClr(this);"> <span id="cap_TAABAAB">Author(s)</span></a>

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------

    

# openLexis()
# loginLexis()
"http://www.lexisnexis.com/lawschool/research/research.aspx"
"go"
"http://www.lexis.com/research/retrieve?_m=86e2dd2f1d22b126731e13d79e311721&_src=155467&_tcid=155467&_fmtstr=TOC&tcact=initial&svc=toc&_stateList=svc&wchp=dGLbVlb-zSkAA&_md5=2f0f99a45735563cac8e48e5d47615c5"
docUrl = "http://web2.westlaw.com/toc/default.wl?pbc=4BF3FCBE&scdb=PATLAWF&service=TOC&action=CollapseTree&fn=_top&sv=Split&itemkey=I975dc1e0ea3511d8970ffc418816559b&ifm=NotSet&ap=I975dc1e0ea3511d8970ffc418816559b&abbr=PATLAWF&rs=WLW10.08&vr=2.0&rp=/toc/default.wl&mt=44"

# gotoUrl(docUrl)



script = (
     'function clickExpandLinks(source){' + 
     "var links = source.getElementsByTagName('a');" + 
     'var linkCount = links.length;' + 
     'for (var i = 0; i < linkCount; i++)' + 
         'url = links[i].href' + 
         "if (url.search('action=ExpandTree')!=1 {" + 
             '}' + 
     'return wordList;' + 
     '}' + 
     'clickExpandLinks(source);')
    
script = ("x=document.getElementsByTagName('frame')[1];" + 
    "a=x.contentDocument;" + 
    "b=a.body.getElementsByTagName('form')['formControl'];" + 
    "c=b.getElementsByTagName('table')['mLayout_ctl00_mTocTree_ctl00_mTocControl'];" + 
    "c.innerHTML;")
# print runScript(script)


abet = 'abcdefghijklmnopqrstuvwxyz'
first_expand_links = getIndexExpandLinks()




'''
b=str(a[0].contents)
c=BeautifulSoup(b)
d=c(attrs={'alt' : 'Collapse'})
print len(d)
#f=d[0].contents
closeTree=d[0].contents['href']
runScript(closeTree)
'''
# all links with action=ExpandTree
# print x.find('javascript:pToc.opnNd(')
# print x.find('tr id="TA')
"""
print 'tr id="TA'
"""

# print runScript(script)
'''


<a href="javascript:pToc.opnNd('TAAB',1,'1')" target="_self"><img src="/ri/IconShow.gif" width="12" height="12" alt="Expand" border="0" title="" align="bottom" onclick="ihd();" onmouseover="sd('TAAB', this);" onmouseout="dhd();" style="padding-top:2px"></a>

<a href="javascript:pToc.clsNd('TAAB',1,'1')" target="_self"><img src="/ri/IconHide.gif" width="12" height="12" alt="Collapse" border="0" title="" align="bottom" onclick="ihd();" onmouseover="sd('TAAB', this);" onmouseout="dhd();" style="padding-top:2px"></a>


<a href="javascript:void(pToc.tc2dc('TAABAABAABAAB','54MF-5DK0-00SR-P0R5-00000-00','','','1'));" target="_self" name="TAABAABAABAAB" onclick="return chClr(this);"><span id="hdr_TAABAABAABAAB"> 1.1-</span> Introduction</a>
'''

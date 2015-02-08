'''
Created on Aug 13, 2013

@author: sethchase
'''
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/html/xgoogle')
from xgoogle.search import GooglePatentSearch, GoogleScholarSearch, SearchError
path.append('/Users/admin/SERVER2/BD_Scripts/html')
import HTML_API as html # getTagsByAttr,readTable,makeTableFromRows,makeHTML,hyperlink
from webpage_scrape import scraper
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import getFilesFolders
import re
from time import sleep


def get_patents(searchString,saveDir,page=""):
    try:
        gs = GooglePatentSearch(searchString)
        if page=="": gs.page = 850
        else: gs.page=page
        results = gs.get_results()
        #print gs._last_from
        print gs.results_info

        
    except SearchError, e:
        print "Search failed: %s" % e
    
    saved_files=getFilesFolders(saveDir, full=False)
    saved_patents=[]
    for it in saved_files: saved_patents.append(it.replace(".html",""))
    
    br=scraper('mechanize','').browser
    pages,filenames=[],[]
    for it in results:
        #print '"'+it.url.encode("utf8")+'",'
        new_patent=it.url.encode("utf8")[31:31+it.url.encode("utf8")[31:].find("?")]
        #new_patent=it.encode("utf8")[31:31+it.encode("utf8")[31:].find("?")]
        if saved_patents.count(new_patent) == 0:
            filenames.append(new_patent)
            x=br.get_page(it.url.encode("utf8"))
            #x=br.get_page(it.encode("utf8"))
            pages.append(x)
            #print len(x)
    
    for i in range(0,len(pages)):
        f=open(saveDir+filenames[i]+'.html','w')
        f.write(pages[i])
        f.close()
        #break

def get_articles(searchString,saveDir,page=""):
    list_for_table=[]
    try:
        gs = GoogleScholarSearch(searchString)
        if page=="": gs.page = 95
        else: gs.page=page
        results = gs.get_results()

        while True:
            for res in results:
                if res.desc:
                    a= html.hyperlink(res.title.encode("utf8"),res.url.encode("utf8"))
                    list_for_table.append(a+'\n'+res.desc.encode("utf8"))
            sleep(5)
            results = gs.get_results()
            if not results: # no more results were found
                print 'no more results'
                break

            if len(list_for_table) >= 1521: break

    except SearchError, e:
        print "Search failed: %s" % e

    body=html.makeTableFromList(list_for_table,'',width='700')
    saveFile=html.makeHTML(body)

    f=open(saveDir+'googleScholarArticles'+'.html','w')
    f.write(saveFile)
    f.close()


def get_patent_refs(saved_files,workDir):
    for it in saved_files:
       
        x=workDir+it
        f=open(x,'r')
        c=f.read()
        f.close()
         # any expression with "US" and 7 digits
        m=re.findall('US[0-9]{7,}',c)
        return m


# USE SEARCH STRING TO SCRAPE GOOGLE PATENTS

saveDir='/Users/admin/Desktop/'
searchString = '"WTC" "EPA" "data"'
get_articles(searchString,saveDir,page="") # ONLY FETCHES ONE PAGE AT A TIME


# GET ALL PATENT REFERENCES IN A TEXT FILE 

#workDir='/Users/admin/Desktop/patents/'
#saved_files=getFilesFolders(workDir, full=False)
#get_patent_refs(saved_files,workDir)

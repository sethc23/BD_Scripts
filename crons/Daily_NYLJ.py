'''
Created on Sep 25, 2013

@author: sethchase
'''


from datetime import datetime
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from var_checks import internet_on
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from webpage_scrape import scraper
import HTML_API
from emailHTML import send_mail
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import decryptPDF_file, findReplaceFileName, deleteFile, reducePDF_file

from time import sleep

def weekday_urls(page,weekday_num):
    #base = 'http://www.newyorklawjournal.com/pdfwrapper.jsp?sel=NYLJ'
    #print page 'article-text basic-article-text'
    body=HTML_API.getTagsByAttr(page,'div',{ "class" : 'article-text basic-article-text' })
    #print body
    bins=HTML_API.FindAllTags(body,'div')
    #print bins
    todayBin=bins[2+eval(weekday_num)]
    #todayBin=bins[3]
    todayLinks=todayBin.find_all('a')
    useable_links=[]
    for it in todayLinks:
        #print it
        if it.find(".html") == -1: useable_links.append(it.get('href'))
    return useable_links

def get_daily_NYLJ():
    br=scraper('firefox').browser
    #------------goto main page, identify PDF-page url, goto PDF-page url
    baseUrl = 'http://www.newyorklawjournal.com/'
    br.open_page(baseUrl)
    startUrl = 'http://store.law.com/Registration/Login.aspx?source=http://www.newyorklawjournal.com/home'
    br.open_page(startUrl)
    sleep(5)
    #------------LOGIN
    usr = 'schase@cozen.com'
    pw = 'money'
    br.window.find_element_by_name("uid").send_keys(usr)
    br.window.find_element_by_name("upass").send_keys(pw)
    br.window.find_element_by_name("continueButtonExisting").click()
    sleep(5)
    z=br.source()
    h=HTML_API.getSoup(z)
    text='New York Law Journal Download Center'
    for it in h.find_all('a',href=True):
        if it.get_text().find(text)!= -1:
            gotoUrl = it.get('href')
            break
    br.open_page(baseUrl[:-1]+gotoUrl)
    sleep(5)
    z=br.source()

    #------------Identify PDF download urls and download  
    weekday_num = str(datetime.today().strftime('%w')).lower()
    today_date = str(datetime.today().strftime('%Y.%m.%d'))
    #today_date = '2014.01.10'
    #print weekday_num,today_date
    paths = weekday_urls(z,weekday_num)
    # print 'sunday = 0'
    #paths = weekday_urls(z,'5')
     
    # '''
    files = []
    for it in paths:
        #print it
        #it = paths[0]
        #print it
        savePath = '/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/'
        if it.find('=') != -1:  saveFile = it[it.rfind('=') + 1:] + '.pdf'
        else: saveFile = it[it.rfind('/') + 1:].rstrip('.pdf') + '.pdf'
        filepath = savePath + saveFile
        files.append(filepath)
        br.window.find_element_by_xpath("//a[contains(@href,'"+it+"')]").click()
        # print "//a[contains(@href,'"+it+"')]"
        sleep(60)
    
    br.quit()

    for it in files:
        findReplaceFileName(savePath, "(1)", "", verbose=False)
        #print '1'
        decryptPDF_file(it)
        #decryptPDF_folder(savePath)
        #print '2'
        #deleteFile(it,confirm=False)
        #deleteFilesWithVar(savePath, ".decrypted", inverse=True, confirm=True)
        findReplaceFileName(savePath, ".decrypted", "", verbose=False)
        #print '3'
        reducePDF_file(it)
        #reducePDF_folder(savePath)
        #print '4'
        deleteFile(it,confirm=False)
        #deleteFilesWithVar(savePath, "_reduced", inverse=True, confirm=True)
        findReplaceFileName(savePath, "_reduced", "", verbose=False)
    
    # send_mail('seth.t.chase@gmail.com', [
    # #    'nadams@cozen.com',
    # #    'EAllagoa@cozen.com',
    # #    'jbeckerman@cozen.com',
    # #    'eberger@cozen.com',
    # 'schase@cozen.com',
    # #    'MCiccia@cozen.com',
    # #    'RFama@cozen.com',
    # #    'RGreebel@cozen.com',
    # 'AHack@cozen.com',
    # 'ally_hack@yahoo.com',
    # 'rkearney@cozen.com',
    # #    'GKnight@cozen.com',
    # #    'MKohel@cozen.com',
    # #    'JMcDonough@cozen.com',
    # 'ANelson@cozen.com',
    # #    'VPozzuto@cozen.com',
    # #    'MSavino@cozen.com',
    # 'dshimkin@cozen.com',
    # 'psardino@cozen.com'
    # #    'Jtierney@cozen.com',
    # #    'AWeinstein@cozen.com',
    # #    'pzola@cozen.com'
    # ], 'NYLJ - '+today_date, "", files, server="localhost")

    for it in files:
        deleteFile(it, confirm=False)

# try:
#     x = internet_on()
#     # print x
# except:
#     print "no internet"
#     x = False
#  
# #x=False
# if x == True:
#     stop,ct=False,10
#     while stop==False:
#         try:
#             get_daily_NYLJ()
#             stop=True
#         except:
#             sleep(10)
#             ct-=1
#             if ct == 0: stop=True
#             else: print 'failed'

x=get_daily_NYLJ()
#print x
# savePath='/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/'
# deleteFilesWithVar(savePath,".decrypted",inverse=True,confirm=False)
# findReplaceFileName(savePath,".decrypted","",verbose=False)
# reducePDF_folder(savePath)
# deleteFilesWithVar(savePath,"_reduced",inverse=True,confirm=False)
# findReplaceFileName(savePath,"_reduced","",verbose=False)
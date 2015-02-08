import urllib2
from os import system
from ftplib import FTP
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from var_checks import internet_on

try:
    x = internet_on()
    # print x
except:
    # print 'no internet'
    x = False

if x == True:
    url = 'http://ipchicken.com/'
    content = urllib2.urlopen(url).read()

    s1 = content.find('<p align="center"')
    s = content.find('<b>', s1) + 3
    e = content.find('<br>', s)
    ipAddress = content[s:e].strip()
    # print ipAddress

    saveFile = 'settings.xml'
    localFilePath = '/Users/admin/SERVER2/BD_Scripts/crons/' + saveFile

    f = open(localFilePath, 'r')
    xmlFile = f.read()
    f.close()
    # print xmlFile
    s = xmlFile.find("sethchase")
    s1 = xmlFile[:s].rfind('ADDRESS="') + len('ADDRESS="')
    e = xmlFile.find('"', s1)
    xmlAddressIP = xmlFile[s1:e]
    # print xmlAddressOld
    
    # currentIP_Url='http://sanspaperllc.com/seth/settings.xml'
    # currentURL_IP = urllib2.urlopen(currentIP_Url).read()
    # print currentURL_IP
    
    # '''
    if xmlAddressIP != ipAddress:  # or xmlAddressIP != currentURL_IP:
        # print 'pass'
        xmlFile = xmlFile.replace(xmlAddressIP, ipAddress)
        
        f = open(localFilePath, 'w')
        f.write(xmlFile)
        f.close()
    
        ftp = FTP('sanspaperllc.com', 'sanspaperllc', 'MoneyTree2012')
        ftp.cwd('/sanspaper/seth')
        f = open(localFilePath, "rb")
        ftp.storbinary('STOR ' + saveFile, f)
        f.close()
        ftp.quit()
    # '''

import os
from appscript import *
from time import sleep
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')

from Adobe_API import startAcrobat, quitAcrobat, doScript, doScriptReturn
from Adobe_API import newPDF, openFile, closePDF
from Adobe_API import insertPages_Bookmark, runOCR, renamePDF

def deleteFirstPage():
    script = ('this.deletePages({});')
    doScript(script)


app(u'Finder').activate()
files = app(u'Finder').selection.get()
fileNames, fileTypes, filePaths = [], [], []

try:
    for arg in sys.argv:
        printPerPage = arg
except:
    pass

for item in files:
    item = str(item)
    fileNames.append(item[item.rfind('[') + 3:item.rfind('[') + item[item.rfind('['):].rfind('.')])
    fileTypes.append(item[item.rfind('.') + 1:item.rfind("'")])
    path = '/'
    for part in item.split('folders[u'):
        if part[0] == "'":
            path = path + part[1:part[2:].find("'") + 2] + '/'
    filePaths.append(path)

startAcrobat()
sleep(1.5)
try:
    app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].click()
except:
    pass
sleep(.5)
newPDF()

'''
create script to convert non-pdf to pdf and include in conversion
include OCR option

for i in range(0,len(fileNames)):
    fileOpen = filePaths[0]+fileNames[0]+"."+fileTypes[0]
    fileSave = fileNames[0]+'.pdf'
    #openFile(fileOpen)
    insertPages(fileOpen)
'''

for i in range(0, len(fileNames)):
    fileOpen = filePaths[i] + fileNames[i] + "." + fileTypes[i]
    fileSave = fileNames[i] + '.pdf'
    # openFile(fileOpen)
#    insertPages(fileOpen)
#    addBookmark(fileNames[i])
    insertPages_Bookmark(fileOpen, fileNames[i])


deleteFirstPage()
renamePDF(filePaths[0] + 'all_docs.pdf')
closePDF()
quitAcrobat()

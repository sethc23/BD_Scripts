import os
from appscript import *
from time import sleep

def startAcrobat():
    app(u'Adobe Acrobat Professional').activate()

def quitAcrobat():
    app(u'Adobe Acrobat Professional').quit() 

def doScript(x):
    app(u'Adobe Acrobat Professional').activate()
    app(u'Adobe Acrobat Professional').do_script(x)

def doScriptReturn(x):
    app(u'Adobe Acrobat Professional').activate()
    return app(u'Adobe Acrobat Professional').do_script(x)

def newPDF():
    script = ('var myDoc = app.newDoc();')
    doScript(script)

def openFile(fileName):
    script = (
     'var filePath = "' + fileName + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function openPDF(filePath){' + 
     'try {' + 
     'app.openDoc({ ' + 
     'cPath: filePath, ' + 
     'bUseConv: true ' + 
     '})' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'openPDF(filePath);')
    doScript(script)

def closePDF():
    script = ('this.closeDoc(true);')
    doScript(script)

def insertPages_Bookmark(filePath, filename):
    script = (
     'var filePath = "' + filePath + '";' + 
     'var filename = "' + filename + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function insertThis(filePath,filename){' + 
     'try {' + 
     'var first = this.pageNum;' + 
     'var before = this.numPages;' + 
     'var place = before - 1;' + 
     'var next = place+1-1;' + 
     'this.insertPages({' + 
     'nPage: place, cPath: filePath, ' + 
     '});' + 
     'var after = this.numPages;'
     'var mark = this.numPages;' + 
     # if not zero, make bm zero, otherwise, make BM the last index
     # 'var bm = bookmarkRoot.children.length - 1;'+
     'this.bookmarkRoot.createChild(filename, "this.pageNum="+next);' + 
     # 'this.pageNum=after;'+
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'insertThis(filePath,filename);')
    doScript(script)

def runOCR():
    app(u'Adobe Acrobat Professional').activate()
    app(u'System Events').processes[u'Acrobat'].menu_bars[1].menu_bar_items[u'Advanced'].menus[1].menu_items[u'Document Processing'].menus[1].menu_items[u'Batch Processing...'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Batch Sequences'].select()
    app(u'System Events').application_processes[u'Acrobat'].key_code(31)
    app(u'System Events').processes[u'Acrobat'].windows[u'Batch Sequences'].buttons[u'Run Sequence'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Run Sequence Confirmation - OCR'].buttons[u'OK'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text - Settings'].buttons[u'OK'].click()

def deleteFirstPage():
    script = ('this.deletePages({});')
    doScript(script)

def renamePDF(filePath):
    script = ('var filePath = "' + filePath + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function saveas(filePath){' + 
     'try {' + 
     'this.saveAs(filePath' + 
     ');' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'saveas(filePath);')
    
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

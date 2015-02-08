import os
from appscript import app
from time import sleep
from sys import path, argv
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from SortStringListByLength import *

adobe = app(u'Adobe Acrobat Professional')
adobeProcess = app(u'System Events').processes[u'Acrobat']
pyShell = app(u'System Events').processes[u'IDLE'].windows[u'Python Shell']

def cleanPath(workPath):
    if workPath.find(':') != -1:
        return workPath.replace(':', '/')
    else: return workPath

def startAcrobat():
    app(u'Adobe Acrobat Professional').activate()
    sleep(2.5)
    try:
        app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].click()
    except:
        click, check = False, 20
        while click == False:
            try:
                app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].click()
                click = True
            except:
                sleep(2)
                check -= 1
                if check == 0:
                    print 'error'
                    raise SystemExit

def quitAcrobat():
    app(u'Adobe Acrobat Professional').quit() 

def openPDF(filePath):
    startAcrobat()
    app(u'Adobe Acrobat Professional').activate()
    app(u'Adobe Acrobat Professional').open(filePath)

def openFile(fileName):
    startAcrobat()
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

def checkFileName(docPath):
    putFolder = "/" + docPath[:docPath.rfind(":")].replace(":", "/")
    putFile = docPath[docPath.rfind(":") + 1:]
    folderContents = os.listdir(putFolder)
    fileIndex = folderContents.count(putFile)
    if fileIndex != 0:
        fileBase = putFile.replace(".pdf", "")
        nextCopy = 0
        for i in range(fileIndex, len(folderContents)):
            if folderContents[i].find(fileBase) != -1:
                nextCopy = nextCopy + 1
        filePath = docPath.replace(".pdf", "(" + str(nextCopy) + ").pdf")
    else:
        filePath = docPath
    return filePath
    

def saveCurrent(refFile):
    app(u'Adobe Acrobat Professional').activate()
    openDocs = app(u'Adobe Acrobat Professional').documents.name.get()
    for i in range(0, len(openDocs)):
        if openDocs[i].find(refFile) == 0:
            docRefInd = i + 1
    app(u'Adobe Acrobat Professional').documents[docRefInd].save()

def savePDF():
    app(u'Adobe Acrobat Professional').documents[1].save(timeout=75000)

def closeFileWindow(fileTitle):
    app(u'Adobe Acrobat Professional').activate()
    openDocs = app(u'Adobe Acrobat Professional').documents.name.get()
    if len(openDocs) == 1:
        docRefInd = 0
    else:
        for i in range(0, len(openDocs)):
            if openDocs[i].find(fileTitle) != 0:
                docRefInd = i    
    app(u'Adobe Acrobat Professional').documents[openDocs[docRefInd]].close()

def deleteOrigFile(filePath):
    origPath = "/" + filePath.replace(":", "/")
    os.remove(origPath)

def closePDF():
    script = ('this.closeDoc(true);')
    doScript(script)
    # app(u'Adobe Acrobat Professional').documents[1].close()
    

def newPDF():
    script = ('var myDoc = app.newDoc();')
    doScript(script)

def doScript(x):
    app(u'Adobe Acrobat Professional').activate()
    app(u'Adobe Acrobat Professional').do_script(x, timeout=2400)

def doScriptReturn(x):
    app(u'Adobe Acrobat Professional').activate()
    return app(u'Adobe Acrobat Professional').do_script(x, timeout=2400)

def doCustScr(x):
    script = (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function customScript(){' + 
     'try {' + 
     
     'var custScr = ' + x + 
      
     'return custScr;' + 
     
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'customScript();')
    custom = doScriptReturn(script)
    return custom

def extract(start, end, filePath):
    script = (
     'var START = ' + str(start) + ';' + 
     'var END = ' + str(end) + ';' + 
     'var FILEPATH = "' + str(filePath) + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function extract(START,END,FILEPATH){' + 
     'try {' + 
     'this.extractPages({' + 
     ' nStart: START,' + 
     ' nEnd: END,' + 
     ' cPath: FILEPATH' + 
     ' });' + 
     '} catch (e) { displayError(e); };' + 
     '}' +  # '')
     'extract(START,END,FILEPATH);')
    # print script
    doScript(script)

def extract_delete(start, end, filePath):
    script = (
     'var START = ' + str(start) + ';' + 
     'var END = ' + str(end) + ';' + 
     'var FILEPATH = "' + str(filePath) + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function delete_extract(START,END,FILEPATH){' + 
     'try {' + 
     'this.extractPages({' + 
     ' nStart: START,' + 
     ' nEnd: END,' + 
     ' cPath: FILEPATH' + 
     ' });' + 
     ' this.deletePages({ nStart: START, nEnd: END });' + 
     '} catch (e) { displayError(e); };' + 
     '}' +  # '')
     'delete_extract(START,END,FILEPATH);')
    # print script
    doScript(script)

def insertAllPages(pageIndex, filePath):
    script = ('var pageIndex = ' + str(pageIndex) + ';' + 
     'var filePath = "' + filePath + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function insertThis(pageIndex,filePath){' + 

     'try {' + 

     'this.insertPages({' + 
     'nPage: pageIndex,' + 
     'cPath: filePath' + 
     '});' + 

     '} catch (e) { displayError(e); }' + 

     '}' + 
     'insertThis(pageIndex,filePath);')
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

def insertPages(sourcePath, args):
    # print filePath
    # if filePath.find('/') != -1: filePath='MacOSX'+filePath.replace('/',':')
    # print filePath
    pageIndex, sourceStart, sourceEnd = None, None, None
    if args[0] != None: pageIndex = args[0]
    if args[1] != None: sourceStart = args[1]
    if args[2] != None: sourceEnd = args[2]
    # nPage = placement of pages on target doc, use -1 for beginning of doc
    # nStart = single/beginning of pages from source doc
    # nEnd = all pages until pt from source doc
    script = 'var filePath = "' + sourcePath + '";'
    if pageIndex != None: script += 'var pageIndex = ' + str(pageIndex) + ';'
    if sourceStart != None: script += 'var sourceStart = ' + str(sourceStart) + ';'
    if sourceEnd != None: script += 'var sourceEnd = ' + str(sourceEnd) + ';'
    script += (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function insertThis(')
    if pageIndex != None: script += 'pageIndex,'
    script += 'filePath'
    if sourceStart != None: script += ',sourceStart'
    if sourceEnd != None: script += ',nEnd'
    script += ('){' + 
         'try {' + 
             'this.insertPages({')
    if pageIndex != None: script += 'nPage: ' + str(pageIndex) + ','
    script += 'cPath: "' + str(sourcePath) + '"'
    if sourceStart != None: script += ',nStart: ' + str(sourceStart)
    if sourceEnd != None: script += ',nEnd: ' + str(sourceEnd)
    script += (
             '});' + 
         '} catch (e) { displayError(e); }' + 
     '}' + 
     'insertThis(')
    if pageIndex != None: script += 'pageIndex,'
    script += 'filePath'
    if sourceStart != None: script += ',sourceStart'
    if sourceEnd != None: script += ',nEnd'
    script += ');'
    # print script
    doScript(script)

def deletePages(start, end=''):
    script = 'var nStart = ' + str(start) + ';'
    if end != '': script += 'var nEnd = ' + str(end) + ';'
    script += (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}')
    script += 'function delete_Pages(nStart,nEnd){'   
    script += (
    'try {')
    script += 'this.deletePages({nStart: nStart'
    if end != '': script += ', nEnd: end_var});'
    else: script += '});'
    script += (
    '} catch (e) { displayError(e); }' + 
    '}')
    if end != '': script += 'deletePages(nStart,nEnd);'
    else: script += 'deletePages(nStart);'
    doScript(script)

def getAllWords():
    script = (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function getPageWords(){' + 
     'try {' + 
     
     'var pgNum = this.pageNum;' + 
     'var wordNum = this.getPageNumWords(pgNum);' + 
     'var wordList="";' + 
     'for (var i = 0; i < wordNum; i++)' + 
         'wordList += (this.getPageNthWord({' + 
             'nPage: pgNum,' + 
             'nWord: i,' + 
             'bStrip: false' + 
             '}) + " ");' + 
     'return wordList;' + 
     
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'getPageWords();')
    allWords = doScriptReturn(script)
    return allWords

def getFirstWords():
    script = (
    'function displayError(x){' + 
    'app.alert({' + 
    'cMsg: "Error! Try again! " + x,' + 
    'cTitle: "Acme Testing Service"' + 
    '});' + 
    '}' + 
    'function getPageWords(){' + 
        'try {' + 
        
            'var pgCount = this.numPages;' + 
            # 'var pgNum = this.pageNum;'+
            # 'var wordNum = this.getPageNumWords(pgNum);'+
            'var wordList="";' + 
            'for (var i=0; i<pgCount; i++) {' + 
                'var wordNum = this.getPageNumWords(i);' + 
                'var added=false;' + 
                'for (var j=0; j<wordNum; j++) {' + 
                    'var newWord = this.getPageNthWord({' + 
                        'nPage: i,' + 
                        'nWord: j,' + 
                        'bStrip: true' + 
                        '});' + 
                    "var newWord = newWord.replace(/^\s+|\s+$/g, '') ;" + 
                    'if (newWord != "")  {' + 
                        'wordList += (" "+ i + ", " + newWord + ": ");' + 
                        'var added=true;' + 
                        'break;' + 
                        '}' + 
                    '}' + 
                'if (added==false)  {' + 
                    'wordList += (" "+ i + ", " + " " + ": ");' + 
                    '}' + 
                '}' + 
            'return wordList;' + 
        '} ' + 
        'catch (e) { displayError(e); }' + 
    '}' + 
    'getPageWords();')
    firstWords = doScriptReturn(script)
    x = firstWords[:-2].split(':')
    pages, words = [], []
    for i in range(0, len(x)):
        y = x[i].split(',')
        pages.append(y[0].strip())
        words.append(y[1].strip()) 
    return pages, words

def getPageCount():
    script = (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function getPageCount(){' + 
     'try {' + 
     'var pgNum = this.numPages;' + 
     'return pgNum;' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'getPageCount();')
    pageCount = doScriptReturn(script)
    return eval(pageCount)

def getPageNum():
    script = (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function getPageCount(){' + 
     'try {' + 
     'var pgNum = this.pageNum;' + 
     'return pgNum;' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'getPageCount();')
    pageNum = doScriptReturn(script)
    return eval(pageNum)

def getPageBounds():
    script = (
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function getPageBounds(){' + 
     'try {' + 
     
     'var test = this.pageWindowRect;' + 
     # 'var test = new Array( "viewState", cVState );'+
     'return test;' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'getPageBounds();')
    return doScriptReturn(script)
    # return eval(doScriptReturn(script))


def movePage(nPage, nAfter):
    script = (
     'var page = "' + str(nPage) + '";' + 
     'var after = "' + str(nAfter) + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function movepage(page,after){' + 
     'try {' + 
     'this.movePage(page,after);' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'movepage(page,after);')
    movePage = doScriptReturn(script)

def moveMultiPage(nStart, nEnd, nAfter):
    script = (
     'var nStart = ' + str(nStart) + ';' + 
     'var nEnd = ' + str(nEnd) + ';' + 
     'var after = ' + str(nAfter) + ';' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function moveMultiPage(nStart,nEnd,after){' + 
     'try {' + 
     'for (var i = 0; i < nEnd-nStart+1; i++)' + 
     'this.movePage({nPage: nStart+i, nAfter: after+i});' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'moveMultiPage(nStart,nEnd,after);')
    moveMultiPages = doScriptReturn(script)

def rotatePage(start, end, degree):
    # degree [0,90,180,270]
    script = (
     'var start = "' + str(start) + '";' + 
     'var end = "' + str(end) + '";' + 
     'var degree = "' + str(degree) + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function rotatePage(start, end, degree){' + 
     'try {' + 
     'this.setPageRotations(start, end, degree);' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'rotatePage(start, end, degree);')
    rotatePage = doScriptReturn(script)

def setupPDFwindow():
    app(u'Adobe Acrobat Professional').activate()
    # set bounds
    # print 'adobe',app(u'Adobe Acrobat Professional').active_doc.bounds.get()
    try:
        f = open('/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/logs/macPrefs.txt', 'r')
        x = f.readlines()
        f.close()
        for it in x:
            if it.split(':')[0] == 'adobe': 
                app(u'Adobe Acrobat Professional').active_doc.bounds.set(eval(it.split(':')[1]))
                break
    except:
        app(u'Adobe Acrobat Professional').active_doc.bounds.set([7, 2, 875, 896])
    # set zoom type
    app(u'Adobe Acrobat Professional').active_doc.PDF_Window.zoom_type.set([k.no_vary])
    # set view to single-page
    app(u'Adobe Acrobat Professional').page_layout.set(u'Single Page')
    # set zoom factor
    app(u'Adobe Acrobat Professional').active_doc.PDF_Window.zoom_factor.set([70])
    # set window position
    app(u'System Events').processes[u'Acrobat'].windows[1].position.set([7, 2])

def setupPYwindow():
    app(u'IDLE').activate()
    sleep(.25)
    app(u'System Events').processes[u'IDLE'].menu_bars[1].menu_bar_items[u'Window'].menus[1].menu_items[1].click()
    sleep(.25)
    app(u'System Events').application_processes[u'IDLE'].windows[1].size.set([520, 602])
    sleep(.25)
    app(u'System Events').application_processes[u'IDLE'].windows[1].position.set([883, 25])
    sleep(.25)

def nextPage():
    app(u'Adobe Acrobat Professional').activate()
    app(u'System Events').application_processes[u'Acrobat'].key_code(124)

def prevPage():
    app(u'Adobe Acrobat Professional').activate()
    app(u'System Events').application_processes[u'Acrobat'].key_code(123)

def gotoPage(pgNum):
    if type(pgNum) != str: pgNum = str(pgNum)
    script = ('var pgNum = "' + pgNum + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function gotoPage(pgNum){' + 
     'try {' + 
     'this.pageNum = pgNum;' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'gotoPage(pgNum);')
    doScript(script)

def firstPage():
    gotoPage(0)
    # app(u'Adobe Acrobat Professional').activate()
    # app(u'System Events').application_processes[u'Acrobat'].key_code(115)


def runPageOCR(pages='all'):
    app(u'Adobe Acrobat Professional').activate()
    sleep(.5)
    # app(u'System Events').application_processes[u'Acrobat'].menu_bars[1].menus[u'Document'].click()
    # sleep(.1)
    app(u'System Events').application_processes[u'Acrobat'].key_code(120, using=k.control_down)
    sleep(.1)
    for i in range(0, 5): app(u'System Events').application_processes[u'Acrobat'].key_code(124)
    sleep(.1)
    for i in range(0, 13): app(u'System Events').application_processes[u'Acrobat'].key_code(125)
    sleep(.1)
    app(u'System Events').application_processes[u'Acrobat'].key_code(124)
    sleep(.1)
    app(u'System Events').application_processes[u'Acrobat'].key_code(36)
    sleep(.1)
    
    # app(u'System Events').application_processes[u'Acrobat'].menu_bars[1].menus[u'Document'].menu_items[u'OCR Text Recognition'].click()
    # sleep(.1)
    # app(u'System Events').application_processes[u'Acrobat'].menu_bars[1].menus[u'Document'].menu_items[u'OCR Text Recognition'].menus[1].menu_items[u'Recognize Text Using OCR...'].click()
    # sleep(.1)
    # app(u'System Events').processes[u'Acrobat'].menu_bars[1].menu_bar_items[u'Document'].menus[1].menu_items[u'OCR Text Recognition'].menus[1].menu_items[u'Recognize Text Using OCR...'].click()
    # app(u'System Events').processes[u'Acrobat'].menu_bars[1].menu_bar_items[u'Document'].menus[1].menu_items[u'OCR Text Recognition'].menus[1].menu_items[u'Recognize Text Using OCR...'].click()
    sleep(.5)
    if pages == 'current':
        ct = 20
        while ct != 0:
            try:
                app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text'].groups[1].radio_buttons[u'Current page'].click()
                app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text'].buttons[u'OK'].click()
                return
            except:
                ct -= 1
                if ct == 0: 
                    print 'error in OCR'
                    return False
                sleep(.5)
    else: 
        ct = 20
        while ct != 0:
            try:
                app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text'].groups[1].radio_buttons[u'All pages'].click()
                app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text'].buttons[u'OK'].click()
                return
            except:
                ct -= 1
                if ct == 0: 
                    print 'error in OCR'
                    return False
                sleep(.5)

def runBatchOCR():
    app(u'Adobe Acrobat Professional').activate()
    app(u'System Events').processes[u'Acrobat'].menu_bars[1].menu_bar_items[u'Advanced'].menus[1].menu_items[u'Document Processing'].menus[1].menu_items[u'Batch Processing...'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Batch Sequences'].select()
    app(u'System Events').application_processes[u'Acrobat'].key_code(31)
    app(u'System Events').processes[u'Acrobat'].windows[u'Batch Sequences'].buttons[u'Run Sequence'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Run Sequence Confirmation - OCR'].buttons[u'OK'].click()
    app(u'System Events').processes[u'Acrobat'].windows[u'Recognize Text - Settings'].buttons[u'OK'].click()

def getFolderPDFCount(workDir):
    fileName, pgCount = [], []
    for it in workDir:
        it = cleanPath(it)
        openFile(it)
        fileName.append(it[it.rfind('/') + 1:])
        pgCount.append(getPageCount())
        closePDF()
    return fileName, pgCount

def zipSinglePDF(filePath=''):
    # zipSingleFile()
    #   deleteFirstPage()
    #   renamePDF(savePath)
    #   closePDF()
    #   quitAcrobat()
    if filePath == '':  
        print "need filepath"
        return
    elif os.path.exists(filePath) != True:
        print 'error in filepath'
        return
    openPDF(filePath)
    pageCount = getPageCount()
    # print pageNum,type(pageNum)
    docHalf = int(round(float(pageCount) / 2.0))
    # print docHalf,type(docHalf)
    pt = 1
    # if str(docHalf).find('.0') != -1:
    for j in range(0, pageCount - docHalf):
        # print 'moving',pageCount-1,'to',j+pt-1
        movePage(pageCount - 1, j + pt - 1)
        pt += 1
    
    if filePath != '':  
        savePDF()
        closePDF()
    
    return 'success'

def zipTwoFilesIntoPDF():
    # zipTwoFiles()
    #  renamePDF(savePath)
    #  closePDF()
    #  quitAcrobat()
    path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
    import API_system
    fileNames, fileTypes, filePaths = API_system.get_files_in_selection()
    
    pop = []
    for i in range(0, len(filePaths)):
        if fileNames[i].find('DS') == -1: pop.append(i)
    
    pop.sort()
    pop.reverse()
    for it in pop: x = fileNames.pop(it), fileTypes.pop(it), filePaths.pop(it)
    
    startAcrobat()
    sleep(2.5)
    try:
        app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].click()
    except:
        pass
    sleep(.5)
    
    '''
    create script to convert non-pdf to pdf and include in conversion
    include OCR option
    
    for i in range(0,len(fileNames)):
        fileOpen = filePaths[0]+fileNames[0]+"."+fileTypes[0]
        fileSave = fileNames[0]+'.pdf'
        #openFile(fileOpen)
        insertPages(fileOpen)
    '''
    
    print len(fileNames)
    iterNum = len(fileNames) / 2
    print 'iter:', iterNum
    print ''
    
    pt = 0
    for i in range(0, iterNum):
        fileOpen = filePaths[pt] + fileNames[pt] + "." + fileTypes[pt]
        fileSave = fileNames[pt][:-3] + '.pdf'
        savePath = filePaths[pt] + fileSave
        pt += 1
        addFilePath = filePaths[pt] + fileNames[pt] + "." + fileTypes[pt]
        pt += 1
        print fileOpen
        print '--', addFilePath
        print '-- --', savePath
        print ''
    
        openFile(fileOpen)
        pageCount = getPageCount()
        sleep(1.5)
        # print pageNum,type(pageNum)
        # print filePaths[i]
        pg_pt = 0
        for j in range(0, pageCount):
            pageIndex, sourceStart = j + pg_pt, pageCount - j - 1
            pg_pt += 1
            # print pageIndex,sourceStart,None
            
            args = pageIndex, sourceStart, None
            insertPages(addFilePath, args)
        renamePDF(savePath)
        closePDF()
        # break


def reversePDF(filePath):
    if filePath == '':  
        print "need filepath"
        return
    elif os.path.exists(filePath) != True:
        print 'error in filepath'
        return
    openPDF(filePath)
    pageCount = getPageCount()
    for j in range(0, pageCount - 1):
        # print 'moving',pageCount-1,'to',j+pt-1
        movePage(0, pageCount - j - 1)  #  nPage, nAfter
    savePDF()
    closePDF()
    return 'success'



# x=doCustScr('app.listMenuItems();')
# x=doCustScr('app.execMenuItem("OptimizerMenuItem");')
# x=getAllWords()
# print x

# app(u'Adobe Acrobat Professional').activate()

# try:
    # x=app(u'System Events').processes[u'Acrobat'].menu_bars[1].menu_bar_items[u'Acrobat'].menus[1].menu_items[u'Preferences...'].name.get()
#    x=app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].name.get()
# except:
#    print 'Fail'

# print x


if __name__ == '__main__':
    try:
        cmd=[]
        cmd.append(os.getcwd()+'/')  
        for i in range(1,len(argv)): cmd.append(argv[i])
            # cmd[0] == current working directory
            # cmd[1] == function to apply
            # cmd[2] == variable for the function
        #print cmd
        stop=False
    except:
        cmd =[]
        pass
        #print 'argument error (or testing)'
        #username,password,command='','',''
        stop=True

    #stop=True

    if cmd == []: stop==True
    if stop == False:
        #print len(cmd), cmd[2],cmd[3]
        if cmd[1] == 'runBatchOCR': runBatchOCR()

   

'''
#openPDF('/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/NYLJmondayA')
openFile('/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/NYLJmondayA')

app(u'Adobe Acrobat Professional').activate()
app(u'System Events').processes[u'Acrobat'].windows[1].checkboxes[u'Do not show this message again'].value.get()

app.execMenuItem("OptimizerMenuItem");
sleep(1)
app(u'System Events').processes[u'Acrobat'].windows[u'PDF Optimizer'].buttons[u'OK'].click()
sleep(1)
app(u'System Events').processes[u'Acrobat'].windows[u'Conversion Warnings'].buttons[u'OK'].click()
sleep(1)
app(u'System Events').processes[u'Acrobat'].windows[u'Save Optimized As'].text_fields[1].value.set('NYLJmondayA_2.pdf')
'''





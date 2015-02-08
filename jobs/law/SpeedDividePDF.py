from sys import argv, path
from os import system, popen, listdir, getcwd
from appscript import *
from time import sleep
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from SortStringListByLength import *
import custom_strings
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
import API_system
path.append('/Users/admin/SERVER2/BD_Scripts/html')
import HTML_API
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from Adobe_API import startAcrobat, quitAcrobat, openPDF, openFile, closePDF
from Adobe_API import doScript, doScriptReturn
from Adobe_API import extract_delete, insertPages, insertAllPages, renamePDF
from Adobe_API import getAllWords, getPageCount, getPageNum, getFirstWords
from Adobe_API import getPageBounds, zipSinglePDF
from Adobe_API import movePage, moveMultiPage, rotatePage, deletePages
from Adobe_API import setupPDFwindow, setupPYwindow
from Adobe_API import nextPage, prevPage, firstPage
from Adobe_API import checkFileName, saveCurrent, closeFileWindow, deleteOrigFile
from Adobe_API import runPageOCR, gotoPage, savePDF
import PDFpenPro_API

from Terminal_API import setupTermWin, getTerminalHistory

adobe = app(u'Adobe Acrobat Professional')
adobeProcess = app(u'System Events').processes[u'Acrobat']
pyShell = app(u'System Events').processes[u'IDLE'].windows[u'Python Shell']

def getFilesFolders(workDir):
    import os
    fileList = []
    x = listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    folders = []
    for i in range(0, len(x)):
        if os.path.isdir(x[i]): folders.append(workDir + x[i])
        else: fileList.append(workDir + x[i])
    while len(folders) != 0:
        newWorkDir = folders[0] + '/'
        x = listdir(newWorkDir)
        try: a = x.pop(x.index('.DS_Store'))
        except: pass
        for i in range(0, len(x)):
            if os.path.isdir(x[i]): folders.append(newWorkDir + x[i])
            else: fileList.append(newWorkDir + x[i])
        a = folders.pop(0)
    return fileList

def getLocalInfo():
    return '/Users/admin/Dropbox/BAYL-DOLE/fileIndexListing.txt'

def combinePDFSupps(get_folder):
    # get_folder="/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR"
    put_folder = get_folder + '/parts_combined'
    workDir1 = get_folder
    '''
    find partial files
    copy partial files to other folder
    '''
    x = listdir(workDir1)
    exclude = [".DS_Store"]
    for item in exclude:
        if x.count(item) != 0:  x.pop(x.index(item))
    # print len(x)
    fileUnit, fileList = [], []
    for it in x:
        y = it.split('_')[0]
        if fileUnit.count(y) == 0:
            fileUnit.append(y)
        else: 
            # if it.find('_L') == -1 and it.find('_C') == -1: 
            fileList.append(it)
                
    print fileList[0]
    # print fileUnit[0]
    # add part 2 to part 1, move part 2 to another folder
    # '''
    combined = []
    for it in fileList:
        z = it.split('_')[1]
        # origFileName=z+'_001'
        origFileName = it.replace('_' + z, '_001') + '.pdf'  # it.split('_')[0]+'_'+it.split('_')[1],it.split('_')[0]+'_001')
        javaPath = get_folder + '/' + origFileName
        
        print javaPath
        # '''
        openFile(javaPath)
        lastPg = getPageCount() - 1
        pageIndex, sourceStart, sourceEnd = lastPg, None, None
        insert_vars = pageIndex, sourceStart, sourceEnd
        insertPages(get_folder + '/' + it, insert_vars)
        javaPath = put_folder + '/' + it
        savePDF()
        closePDF()
        # '''
        fromPath = get_folder + '/' + it
        toPath = put_folder + '/' + it
        print 'fromPath', fromPath
        print 'toPath  ', toPath
        if API_system.checkFilePathExists(toPath) == False: system('mv ' + fromPath + ' ' + toPath)
        else: print 'check', toPath        
        # break
    # '''
        

#### NEEDS LOTS OF WORK
def reOrderPages():
    page, wordNum, word = [], [], []
    pgVars = []
    for i in range(0, len(PAGES)):
        page = i
        wordNum, word = [], []
        # --**--  check to confirm words on pages include numbers
        pageWords = getAllWords()
        for j in range(0, len(pageWords)):
            if pageWords[j].isdigit():
                wordNum, word = j, pageWords[j]
        pgVars.append(page, wordNum, word)
        
        for it in false_match:
            if page[0].count(it) != 0:
                page[0].pop(page[0].index(it))
        
        for it in page[i]:
            if page[i + 1].count(it) != 0:
                if match.count(it) == 0:
                    match[i].append(it)
                    match[i + 1] = match[i + 1] + 1
                    if match[i + 1] >= .1 * len(PAGES):
                        test = check_match(match)
                        if test == False:
                            false_match.append(match)
                        else: 
                            return run_sort(match)
                            
    # notes
    '''                   
                #else: match_counter.append([it
        
        #for it in match:
        
#identify spaces/characters between number and beginning/end
#identify number of pages           
        
    #m_pt=  # set 
    
    for i in range(0,len(pgVars[0])):
        for j in range(0,len(pgVars[1])):
            #check to see if next page has any digits with same number
        #checkPgVars(pgVars)


def checkPgVars(pgVars):
    # pgVars = page,wordNum,word
    
    for i in range(0,len(pgVars[0])):
        for j in range(0,len(pgVars[1])):
                     
    
        PgVar = identify numbers in first page



for each of those number placements:
	check placement in next page with 5% margin on placement
	if zero matches,
		start with this page as new number template (save previous results), go to next page
	elif some matches,
		remove all non-matches, go to next page
		
'''		

def getDirListing():
    localFilePath = getLocalInfo()
    f = open(localFilePath, 'r')
    x = f.readlines()
    f.close()
    y = [it.rstrip('\n') for it in x]
    return y

def appendDirListing(content):
    localFilePath = getLocalInfo()
    f = open(localFilePath, 'a')
    f.write(content + '\n')
    f.close()

def updateDirListing(dir1):
    localFilePath = getLocalInfo()
    prevList = getDirListing()
    # print 'prev',prevList
    currList = listdir(dir1)
    # print 'curr',currList
    exclude = [".DS_Store", "1_unzipped", "parts_combined", "AUTM_2004", "AUTM_2005"]
    for it in exclude:
        if currList.count(it) != 0:  currList.pop(currList.index(it))
    popList = []
    for i in range(0, len(currList)):
        it = currList[i]
        it = it.replace('\n', '')
        if prevList.count(it) != 0:  
            popList.append(i)
    popList.sort()
    popList.reverse()
    x = [currList.pop(it) for it in popList]
    newList = prevList
    if len(currList) != 0:
        f = open(localFilePath, 'a')
        for it in currList:
            it = it.replace('\n', '')
            f.write(it + '\n')
            newList.append(it)
        f.close()
    return newList

def findRepeats(macEPath, keyword):
    useKeyword = True
    while useKeyword == True:
        print "...checking keyword..."
        print ""
        app(u'Terminal').activate()
        # keyword = str(raw_input("")).lower()
        keyword = keyword.lower()
        # print ""
        extracted = getDirListing()
        # extracted = listdi#r("/"+macEPath.replace(':','/'))
        xLower = str(extracted).lower()
        xLower = xLower.replace('_COPY', '').replace('_ADD', '')
        x = str(extracted)
        fileNames, p = [], 0
        for i in range(0, xLower.count(keyword)):
            KWref = xLower.index(keyword, p)
            LMref = xLower.rfind("'", 0, KWref)
            RMref = xLower.find("'", KWref)
            p = KWref + 1
            nameFile = x[LMref + 1:RMref - 4]           
            if (nameFile[len(nameFile) - 3] == '(' and nameFile[len(nameFile) - 2].isdigit() == True
             and nameFile[len(nameFile) - 1] == ')'):
                pass
            elif (nameFile[len(nameFile) - 4] == '(' and nameFile[len(nameFile) - 3:len(nameFile) - 2].isdigit() == True
             and nameFile[len(nameFile) - 1] == ')'):
                pass
            elif (nameFile.find('_COPY') != -1 or
                nameFile.find('_ADD') != -1 or
                nameFile.find('_CHECK') != -1):  # both being -1
                pass
            else:
                fileNames.append(nameFile)
                print "(-" + str(len(fileNames)) + ")  " + nameFile
        if fileNames == []:
            print "No results from Search"
        print ""
        print "Type '-number', Another Keyword:'a', or Go Back:'-g'"
        print ""
        app(u'Terminal').activate()
        result = str(raw_input(""))
        print ''
        if result[0] == "-":
            if result[1] == 'g':
                return "again"
                # newDoc(macEPath,docPgCount,fileName)
            else:
                print "(1)  Copy of Document;\n(2)  Additional Documentation; or\n(3)  Not sure."
                add_copy = str(raw_input("\n:  "))
                print '\n'
                thisFile = fileNames[eval(result[1:]) - 1]
                date = thisFile[:thisFile.find(' - ')]
                title = thisFile[thisFile.find(' - ') + 3:]
                useKeyword = False
                if add_copy == '1':   title = title + '_COPY'
                if add_copy == '2':   title = title + '_ADD'
                if add_copy == '3':   title = title + '_CHECK'
        elif result == 'a':
            keyword = str(raw_input("\nKeyword?\n\n:  "))
            print ''
        elif result == 'q':
            date, title = '', ''
            useKeyword = False
    return date, title

def getDates(macEPath, keydate):
    extracted = getDirListing()
    x = str(extracted).replace('\n', '')
    fileNames, p = [], 0
    for i in range(0, str(extracted).count(keydate)):
        KWref = x.index(keydate, p)
        LMref = x.rfind("'", 0, KWref)
        RMref = x.find("'", KWref)  # -2 #not sure why adding, but added after using listdir which add '\n'
        p = KWref + 1
        nameFile = x[LMref + 1:RMref - 4]
        if (nameFile[len(nameFile) - 3] == '(' and nameFile[len(nameFile) - 2].isdigit() == True
             and nameFile[len(nameFile) - 1] == ')'):
            pass
        elif (nameFile[len(nameFile) - 4] == '(' and nameFile[len(nameFile) - 3:len(nameFile) - 2].isdigit() == True
             and nameFile[len(nameFile) - 1] == ')'):
            pass
        else:
            fileNames.append(nameFile)
            print "( -" + str(len(fileNames)) + " )  " + nameFile
    if fileNames == []:
        print "(no previous files with date)"
    return fileNames

def getDateAndTitle(macEPath):
    app(u'Terminal').activate()
    print "Date of Document? (format: 'yyyy.mm.dd') Or type keyword"
    print ""
    date_keyword = str(raw_input(""))
    if date_keyword == 'ND': date_keyword = '0000.00.00'
    print ""
    if date_keyword[0].isdigit() == True:
        date = date_keyword
        if len(date) < 8:
            if date[2] != '.':
                date = "0" + date
            if date[5] != '.':
                date = date[:3] + '0' + date[3:]
            if len(date) == 7:
                date = date + '0'
        fileNames = getDates(macEPath, date)
    if date_keyword[0].isdigit() == False:
        keyword = date_keyword
        result = findRepeats(macEPath, keyword)
        if type(result) != list:
            if result == 'again': return 'again'
        date, title = result
        # date,title = findRepeats(macEPath,keyword)
        if date == '' and title == '':
            return False
    else:
        firstPage()
        sleep(.25)
        app(u'Terminal').activate()
        print ""
        print "type 'Title of Document' or '-number' or Go Back:'-g'"
        print ""
        title = str(raw_input(""))
        print ''
        exclude = ['"', "'", ':', '/', '&', '@', '#', '*']
        for it in exclude:
            if title.find(it) != -1:
                print "Sorry '", it, "' is not a valid character for a Filename/Title\n"
                return "again"
        if title[0] == "-":
            if title[1] == 'g':
                return "again"
                # newDoc(macEPath,docPgCount,fileName) 
            else:
                print "(1)  Copy of Document;\n(2)  Additional Documentation; or\n(3)  Not Sure.\n"
                add_copy = str(raw_input("\n:  "))
                print '\n'
                thisFile = fileNames[eval(title[1:]) - 1]
                date = thisFile[:thisFile.find(' - ')]
                title = thisFile[thisFile.find(' - ') + 3:]
                if add_copy == '1':   title = title + '_COPY'
                if add_copy == '2':   title = title + '_ADD'
                if add_copy == '3':   title = title + '_CHECK'
    return date, title
                

def newDoc(macEPath, docPgCount, fileName):
    result = getDateAndTitle(macEPath)
    if type(result) != list:
        while result == 'again':
            result = getDateAndTitle(macEPath)
    date, title = result
    start, end = 0, (docPgCount - 1)
    date_title_label = date + " - " + title
    cleanFileName = checkFileName(macEPath + ":" + date_title_label[:255] + ".pdf")
    newFilePath = ("/" + cleanFileName).replace(':', '/')
    # print start,end,newFilePath
    extract_delete(start, end, newFilePath)
    appendDirListing(newFilePath[newFilePath.rfind('/') + 1:])
    # print 'done'
    return True

def renameDoc(macEPath, fileName, filePath):
    result = getDateAndTitle(macEPath)
    if type(result) != list:
        while result == 'again':
            result = getDateAndTitle(macEPath)
    date, title = result
    date_title_label = date + " - " + title
    cleanFileName = checkFileName(macEPath + ":" + date_title_label[:255] + ".pdf")
    newFilePath = ("/" + cleanFileName).replace(':', '/')
    renamePDF(newFilePath)
    appendDirListing(newFilePath[newFilePath.rfind('/') + 1:])
    closeFileWindow(cleanFileName[cleanFileName.rfind(':') + 1:])
    # system('rm '+'/'+filePath.replace(':','/'))
    fromPath = filePath.replace(':', '/')
    toPath = fromPath.replace('3_DIV_SCAN', '0_ORIG')
    system('mv ' + fromPath + ' ' + toPath)
    # if API_system.checkFilePathExists(toPath) == False: system('mv '+fromPath+' '+toPath)
    # else: print 'check',toPath
    return True

def reOCRwithRotation(folder):
    for k in range(1419, len(folder)):
        # filePath='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR/0069_001_OCR.pdf'
        # fileName=filePath[filePath.rfind('/')+1:]
        fileName = folder[k]
        filePath = workDir + '/' + fileName
        
        PDFpenPro_API.openPDF(filePath)
        pgWidths = PDFpenPro_API.getPageWidth()
        pgHeights = PDFpenPro_API.getPageHeight()
        PDFpenPro_API.closeWindow()
        
        openPDF(filePath)
        pages, words = getFirstWords()
        popList = []
        for i in range(0, len(pages)):
            if words[i] != 'null': popList.append(i)
            elif pgHeights[i] > pgWidths[i]: popList.append(i)
            
        popList.sort()
        popList.reverse()
        for it in popList:
            pages.pop(it)
            words.pop(it)
        print k, fileName, pages
        for i in range(0, len(words)):
            runCheck = True
            gotoPage(pages[i])
            while runCheck == True:
                rotatePage(pages[i], pages[i], 90)
                step = runPageOCR('current')
                if step == False: runCheck = False
                # sleep(1.5)
                newWords = getAllWords()
                if newWords.strip().isdigit() == True:
                    savePDF()
                    runCheck = False
                if runCheck == False: break
                for it in DIVIDER_words:
                    if newWords.find(it) >= 0:
                        savePDF()
                        # print '--1'
                        # print asdas
                        runCheck = False
                if runCheck == False: break
                rotatePage(pages[i], pages[i], 180)
                runPageOCR('current')
                newWords = getAllWords()
                for it in DIVIDER_words:
                    if newWords.find(it) >= 0:
                        savePDF()
                        # print '--2'
                        # print asdsa
                        runCheck = False
                if runCheck == False: break
                # closePDF()
                # openPDF(filePath)
                runCheck = False
        closePDF()

def DivideByPageContent(orig_folder, get_folder, put_folder, words, labels):
    # if no divider pages, moves files to put_folder with "_DIV" added to filename
    # if divider pages
        # for all sections with 'double' divider pages, moves files to put_folder with "_DBL"+i added to filename
        # for all sections with 'next' divider pages, moves files to put_folder with "_NeXT"+i added to filename
        # moves original file to orig_folder with "_SPL" added to filename
    workDir0 = '/' + orig_folder.replace(':', '/')
    workDir1 = '/' + get_folder.replace(':', '/')
    workDir2 = '/' + put_folder.replace(':', '/')
    dirContent = listdir(workDir1.rstrip())
    exclude = [".DS_Store"]
    for item in exclude:
        if dirContent.count(item) != 0:  dirContent.pop(dirContent.index(item))
    for k in range(0, len(dirContent)):
        filename = dirContent[k]
        filePath = workDir1 + '/' + filename
        openPDF(filePath)
        # setupPDFwindow()
        x = getFirstWords()
        splitDocInd = []
        for it in words:
            pt = 0
            for i in range(0, x[1].count(it)):
                page_i = x[1].index(it, pt)
                splitDocInd.append(eval(x[0][page_i]))
                pt = page_i + 1
        if len(splitDocInd) == 0: 
            filename2 = filename[:-4] + '_DIV.pdf'
            closePDF()
            fromPath = workDir1 + '/' + filename
            toPath = workDir2 + '/' + filename2
            print 'fromPath', fromPath
            print 'toPath  ', toPath
            # if checkFileExists(toPath) == False: system('mv '+fromPath+' '+toPath)
            # else: print 'check',toPath
        else:
            splitDocInd.sort()
            added = False
            if splitDocInd[0] != 0:  # in case file remaining file started without label, but later had labels
                splitDocInd.append(0)
                splitDocInd.sort()
                added = True
            splitDocInd.reverse()
            next_count, dbl_count, pull_pgCount = 0, 0, 0
            for i in range(0, len(splitDocInd)):
                page_i = eval(x[0][splitDocInd[i]])
                word_i = x[1][splitDocInd[i]]
                # if i == len(splitDocInd) - 1: # if last iteration (first document)
                #    if splitDocInd[i] != 0: previous=0  #if first doc not start on page 0, start page zero
                #    else: previous=1 #else
                previous = page_i + 1
                # if previous==0: previous=1
                if added == True: 
                    if i == len(splitDocInd) - 1: previous = 0  # correction for added mentioned above
                if i == 0: end = eval(x[0][len(x[0]) - 1])
                else: end = splitDocInd[i - 1] - 1
                if word_i.strip() == 'NEXT':
                    label = '_NEXT_' + str(next_count)
                    next_count += 1
                elif word_i.strip() == 'DOUBLE':
                    label = '_DBL_' + str(dbl_count)
                    dbl_count += 1
                pull_pgCount += end - previous    
                newFileName = filename[:-4] + label + '.pdf'
                newFilePath = put_folder + newFileName
                javapath = '/' + newFilePath.replace(':', '/')
                # print label,previous,end
                # extract_delete(previous,end,javapath)
            pgCount = getPageCount()
            if pgCount == next_count + dbl_count: print 'success count', filename
            else: print '----------check count:', filename
            closePDF()
            filename0 = filename[:-4] + '_SPL.pdf'
            fromPath = workDir1 + '/' + filename
            toPath = workDir0 + '/' + filename0
            print 'fromPath', fromPath
            print 'toPath  ', toPath
            # if checkFileExists(toPath) == False: system('mv '+fromPath+' '+toPath)
            # else: print '----------check put_path:',toPath
            break

def runSpeedDivide():
    workDir0 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
    workDir1 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
    # /1_unzipped
    workDir2 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR'
    # /parts_combined
    workDir3 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/3_DIV_SCAN'
    workDir4 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/4_PREPPED_FILES'
    workDir5 = '/Users/admin/Desktop/fix'
    
    macPath = workDir3
    get_folder, put_folder = workDir3, workDir4
    macWPath, macEPath = workDir3[1:].replace('/', ':'), workDir4[1:].replace('/', ':')

    # subDir=listdir(workDir4)
    dirContent = listdir(workDir3)
    print '\nFiles Remaining:', len(dirContent), '\n'

    exclude = [".DS_Store", "1_unzipped", "parts_combined", "AUTM_2004", "AUTM_2005"]
    for item in exclude:
        # if subDir.count(item)!=0: subDir.pop(subDir.index(item)
        if dirContent.count(item) != 0: dirContent.pop(dirContent.index(item))
    fileList = []
    # setupPYwindow()
    setupTermWin()
    print ""
    worker = raw_input("\n Your Name:  ")
    print ''
   # for i in range(0,len(subDir)):
   #     dirContent = listdir(workingDir+"/"+subDir[i])
   #     exclude = [".DS_Store"]
   #     for item in exclude:
   #         if subDir.count(item)!=0: subDir.pop(subDir.index(item)
   #     if dirContent == []:
   #         pass
   #     else:
            # startFileLen = len(dirContent[0])
            # endFileLen = len(dirContent[len(dirContent)-1])
            # if startFileLen != endFileLen:
            #    dirContent = SortStringListByLength(dirContent)
            # macPath = macWPath+subDir[i]+":"
    startAcrobat()
    newList = updateDirListing(put_folder)
    # #
    # #
    for j in range(0, len(dirContent)):
        filePath = macPath + '/' + dirContent[j]
        # print file
        openPDF(filePath)
        # #runOCR()
        # test = getAllWords()
        setupPDFwindow()
        complete = False
        stop = False
        while complete == False and stop == False:
            docPgCount = 1
            pdfPgCount = getPageCount()
            app(u'Terminal').activate()
            print "Options:"
            options = ["Zip Double Sided", "Create New document from remaining PDF",
            # "Part of Same/Previous document",
                       "Make this last page of document", "Rotate Page(s)", "Delete Page(s)", "Move this Page",
                       "Move multi Pages", "Calculate Pages Reviewed",
                       "Copy to 1000+ Pages to Archive", "Check Archive Folder Docs",
                       "Update folder docs",
                       "Quit"]
            for m in range(0, len(options)):
                print "(" + str(m + 1) + ")  " + options[m]
            print '\n[ file:\t' + dirContent[j] + ' ]\n'
            step = raw_input(":  ")
            print ""
            choice = options[eval(step) - 1]
            sleep(.25)
            if choice == "Zip Double Sided":
                gotoPage(1)
                zipSinglePDF()
            elif choice == "Rotate Page(s)":
                opt1 = raw_input('1.  Rotate only this page.\n2.  Rotate numerous pages.\n\n:  ')
                print ''
                if ['1', '2'].count(opt1) == 0: print 'Please try again\n'
                else:
                    if opt1 == 2:
                        startPage = raw_input("Start rotating on what page?\n\n:  ")
                        print ''
                        endPage = raw_input("End rotating on what page?\n\n:  ")
                        print ''
                    else: startPage, endPage = getPageNum(), getPageNum()
                    app(u'Terminal').activate()
                    opt2 = raw_input("Degrees?   a=90,b=180,c=270\n\n:  ")
                    print ''
                    if ['a', 'b', 'c'].count(opt2) == 0: print 'Please try again\n'
                    else:
                        for it in ['a', 'b', 'c']: 
                            if opt2 == it: 
                                degrees = 90 + 90 * ['a', 'b', 'c'].index(opt2)
                                rotatePage(startPage, endPage, degrees)
                                
            elif choice == "Delete Page(s)":
                opt1 = raw_input('1.  Delete only this page.\n2.  Delete numerous pages.\n\n:  ')
                print ''
                if ['1', '2'].count(opt1) == 0: print 'Please try again\n'
                else:
                    if opt1 == 2:
                        startPage = raw_input("Start deleting on what page?\n\n:  ")
                        print ''
                        endPage = raw_input("End deleting on what page?\n\n:  ")
                        print ''
                    else: startPage, endPage = getPageNum(), getPageNum()
                    app(u'Terminal').activate()
                    deletePages(startPage, endPage)
                                
            elif choice == "Create New document from remaining PDF":
                # docPgCount = getPageNum()+1
                # docPgCount = docPgCount - 1
                # result = newDoc(macEPath,pdfPgCount,dirContent[j])
                result = renameDoc(macEPath, dirContent[j], filePath)
                if result == True: complete = True
                # true - made new file
                # false - type date, or quit
                
            elif choice == "Part of Same document":
                docPgCount = getPageNum() + 1 + 1
                pdfPgCount = getPageCount()
                if docPgCount == pdfPgCount:
                    nextPage()
                    result = renameDoc(macEPath, dirContent[j], filePath)
                    if result == True:
                        complete = True
                else:
                    nextPage()
                    
            elif choice == "Make this last page of document":
                docPgCount = getPageNum() + 1
                pdfPgCount = getPageCount()
                if docPgCount == pdfPgCount:
                    result = renameDoc(macEPath, dirContent[j], filePath)
                    while result == "again":
                        result = renameDoc(macEPath, dirContent[j], filePath)
                    if result == True:
                        complete = True
                else:
                    result = newDoc(macEPath, docPgCount, dirContent[j])
                    while result == "again":
                        result = newDoc(macEPath, docPgCount, dirContent[j])
                    # true - made new file
                    # false - type date, or quit

            elif choice == "Move this Page":
                print "Move this page number what?"
                print ""
                answer = raw_input("")
                nPage = getPageNum()
                nAfter = eval(answer) - 2
                movePage(nPage, nAfter)

            elif choice == "Move multi Pages":
                print "Move pages ... "
                print ""
                print "starting with ?"
                nStart = eval(raw_input("")) - 1
                print "ending with ?"
                nEnd = eval(raw_input("")) - 1
                print ""
                print "Move pages to ?"
                print ""
                nAfter = eval(raw_input("")) - 2
                moveMultiPage(str(nStart), str(nEnd), str(nAfter))

            elif choice == "Calculate Pages Reviewed":
                closeFileWindow(dirContent[j])
                runPageCount()
                openPDF(filePath)
                setupPDFwindow()

            elif choice == "Update folder docs":
                closeFileWindow(dirContent[j])
                app(u'Terminal').activate()
                print "What is the destination folder name?"
                print ""
                folder = str(raw_input(""))
                runUpdateDocs(folder)
                openPDF(filePath)
                setupPDFwindow()

            elif choice == "Copy to 1000+ Pages to Archive":
                closeFileWindow(dirContent[j])
                app(u'Terminal').activate()
                print "What is the destination folder name?"
                print ""
                folder = str(raw_input(""))
                runCopyDocs(folder)
                openPDF(filePath)
                setupPDFwindow()

            elif choice == "Check Archive Folder Docs":
                closeFileWindow(dirContent[j])
                app(u'Terminal').activate()
                print "What is the archive folder name?"
                print ""
                folder = str(raw_input(""))
                runFolderCount(folder)
                openPDF(filePath)
                setupPDFwindow()
                        
            elif choice == "Quit":
                date_time, entry = getTerminalHistory()
                savePath = macPath[:macPath.rfind('/') + 1] + '/logs/' + date_time + '_SpeedDivideLog.txt'
                f = open(savePath, 'w+')
                f.write(entry)
                f.close()
                stop = True
        if stop == True:
            try:
                saveCurrent(dirContent[j])
            except CommandError:
                pass
            break


def runPageCount():
    macWPath = "Users:sethchase:Desktop:PierceLibrary:"
    macEPath = "Users:sethchase:Desktop:PierceLibrary:extracted"
    ArchiveDir = "/Users/admin/Desktop/PierceLibrary/Reports/Archives"
    subDir = listdir(ArchiveDir)
    exclude = [".DS_Store", "Zips"]
    for item in exclude:
        if subDir.count(item) != 0:
            subDir.remove(item)
    ArchiveFileList = []
    for i in range(0, len(subDir)):
        ArchiveFileList.extend(listdir(ArchiveDir + '/' + subDir[i]))
    workDir = "/Users/admin/Desktop/PierceLibrary/extracted"
    newFileList = listdir(workDir)
    for item in exclude:
        if newFileList.count(item) != 0:
            newFileList.remove(item)
    for j in range(0, len(ArchiveFileList)):
        if newFileList.count(ArchiveFileList[j]) != 0:
            newFileList.pop(newFileList.index(ArchiveFileList[j]))
    docCount = len(newFileList)
    pageCount = 0
    for k in range(0, len(newFileList)):
        filePath = macEPath + ':' + newFileList[k] 
        openPDF(filePath)
        pageCount = pageCount + getPageCount()
        closeFileWindow(newFileList[k])
    print ""
    print "There are ", docCount, " documents and ", pageCount, " pages"
    print ""

def runFolderCount(folder):
    macWPath = "Users:sethchase:Desktop:PierceLibrary:"
    macEPath = "Users:sethchase:Desktop:PierceLibrary:extracted"
    ArchiveDir = "/Users/admin/Desktop/PierceLibrary/Reports/Archives/" + folder
    newFileList = listdir(ArchiveDir)
    exclude = [".DS_Store", "Zips"]
    for item in exclude:
        if newFileList.count(item) != 0:
            newFileList.remove(item)
    docCount = len(newFileList)
    pageCount = 0
    for k in range(0, len(newFileList)):
        filePath = macEPath + ':' + newFileList[k] 
        openPDF(filePath)
        pageCount = pageCount + getPageCount()
        closeFileWindow(newFileList[k])
    print ""
    print "There are ", docCount, " documents and ", pageCount, " pages"
    print ""

def runCopyDocs(folder):
    macWPath = "Users:sethchase:Desktop:PierceLibrary:"
    macEPath = "Users:sethchase:Desktop:PierceLibrary:extracted"
    ArchiveDir = "/Users/admin/Desktop/PierceLibrary/Reports/Archives"
    workDir = "/Users/admin/Desktop/PierceLibrary/extracted"
    copyToDir = ArchiveDir + '/' + folder
    subDir = listdir(ArchiveDir)
    if subDir.count(folder) == 0:
        print 'made folder'
        system('mkdir ' + copyToDir)
    exclude = [".DS_Store", "Zips"]
    for item in exclude:
        if subDir.count(item) != 0:
            subDir.remove(item)
    ArchiveFileList = []
    for i in range(0, len(subDir)):
        ArchiveFileList.extend(listdir(ArchiveDir + '/' + subDir[i]))
    for item in exclude:
        if ArchiveFileList.count(item) != 0:
            ArchiveFileList.remove(item)
    newFileList = listdir(workDir)
    exclude = [".DS_Store"]
    for item in exclude:
        newFileList.remove(item)
        ArchiveFileList.remove(item)
    for j in range(0, len(ArchiveFileList)):
        try:
            newFileList.pop(newFileList.index(ArchiveFileList[j]))
        except ValueError:
            print ArchiveFileList[j]
    docCount = len(newFileList)
    pageCount = 0
    for k in range(0, len(newFileList)):
        if pageCount <= 1500:
            filePath = macEPath + ':' + newFileList[k] 
            openPDF(filePath)
            pageCount = pageCount + getPageCount()
            closeFileWindow(newFileList[k])
            fileOSPath = workDir + '/' + newFileList[k]
            fileOSDest = copyToDir + '/' + newFileList[k]
            system("cp '" + fileOSPath + "' '" + fileOSDest + "'")
    print ""
    print "Completed the copy"
    print ""
    

def runUpdateDocs(folder):
    ArchiveDir = "/Users/admin/Desktop/PierceLibrary/Reports/Archives"
    subDir = listdir(ArchiveDir)
    if subDir.count(folder) == 0:
        print 'folder ', folder, ' not found'
        return
    else:
        updateDir = ArchiveDir + '/' + folder
    folderContents = listdir(updateDir)
    exclude = [".DS_Store"]
    for item in exclude:
        if folderContents.count(item) != 0:
            folderContents.remove(item)
    macWPath = "Users:sethchase:Desktop:PierceLibrary:Reports:Archives"
    macEPath = macWPath + ":" + folder
    
    for k in range(0, len(folderContents)):
        MacFilePath = macEPath + ":" + folderContents[k]
        openPDF(MacFilePath)
        rotatePage(0, 0, 180)
        rotatePage(0, 0, 0)
        saveCurrent(folderContents[k])
        closeFileWindow(folderContents[k])
    
    print ""
    print "Completed the updates"
    print ""

def CopyFilesToExcel():
    import os
    from putExcelData import putExcelData
    from numpy import array
    from arrayFin import arrayFin
    from arrayFout import arrayFout
    from listFin import listFin
    macWPath = "Users:sethchase:Desktop:PierceLibrary:Reports:Archives"
    macEPath = "Users:sethchase:Desktop:PierceLibrary:Reports:Archives:"
    workingDir = "/Users/admin/Desktop"
    """
    upDirContent=listdir("/"+macEPath.replace(":","/").rstrip("/"))
    exclude = [".DS_Store","pdfIndex.xls","Zips"]
    for item in exclude:
        while upDirContent.count(item) != 0:
            upDirContent.remove(item)
    fileList = []
    for folder in upDirContent:
        tempDirContents=listdir("/"+macEPath.replace(":","/")+folder)
        for item in exclude:
            while tempDirContents.count(item) != 0:
                tempDirContents.remove(item)
        for fileName in tempDirContents:
            fileList.append(folder+":"+fileName)

    docDate,docTitle,pgCount,docPath = [],[],[],[]

    dirContent = fileList
    for i in range(0,len(dirContent)):
        filePath = macEPath+dirContent[i]
        delimiter = dirContent[i].find(" - ")
        docDate.append(dirContent[i][:delimiter])
        docTitle.append(dirContent[i][delimiter+3:-4])
        openPDF(filePath)
        pgCount.append(getPageCount())
        closeFileWindow(dirContent[i])
        ##docPath.append('<a href="'+"JGpdfs/"+str(dirContent[i])+'">')
        docPath.append("JGpdfs/"+str(dirContent[i]))

    """

    docDate2 = listFin("JGFileData0.txt")
    docTitle2 = listFin("JGFileData1.txt")
    pgCount2 = listFin("JGFileData2.txt")
    docPath2 = listFin("JGFileData3.txt")
    docDate, docTitle, pgCount, docPath = [], [], [], []

    for i in range(0, len(docDate2)):
        date = str(docDate2[i]).rstrip("\n")[docDate2[i].find(":") + 1:].replace(".", "/")
        if int(date[-2:]) < 10 :
            date = date[:-2] + "20" + date[-2:]
        else:
            date = date[:-2] + "19" + date[-2:]
        docDate.append(date)
        docTitle.append(str(docTitle2[i]).rstrip("\n"))
        pgCount.append(str(pgCount2[i]).rstrip("\n"))
        path1 = str(docPath2[i]).rstrip("\n")[0:docPath2[i].find("/") + 1]
        path2 = str(docPath2[i]).rstrip("\n")[docPath2[i].find(":") + 1:]
        docPath.append(path1 + path2)

    excelData = docDate, docTitle, pgCount, docPath
    excelFormat = ['text', 'text', 'number', 'text']
    workbook = workingDir + "/pdfIndex2.xls"
    worksheet = "Sheet1"

    result = putExcelData(workbook, worksheet, excelData, excelFormat)
    print result

def consolidateReps(startDir, endDir):
    ### --- ###
    TEST = False
    # TEST=True
    ### ---  ###
    # FileStartDir = "/Users/admin/Desktop"
    # FileEndDir = "/Users/admin/Desktop"
    FileStartDir, FileEndDir = startDir, endDir
    folderContents = listdir(FileStartDir)
    exclude = [".DS_Store"]
    for item in exclude:
        if folderContents.count(item) != 0:
            folderContents.remove(item)
    stringContents = str(folderContents[:])
    repFiles = [[], [], [], [], []]
    condenseList = []
    for fileName in folderContents:
        if (((fileName[:-4].rfind(")") == len(fileName[:-4]) - 1) or 
            fileName.find('_ADD') != -1) and fileName.find('_AGGR_') == -1):
            # condenseList.append(fileName)
            # if stringContents.count(fileName[:fileName.rfind("(")]) >= 10:
            # if fileName.find('_ADD') == -1:
            if (fileName[:-4].rfind(")") == len(fileName[:-4]) - 1):
                cleanFileName = fileName[:fileName.rfind("(")].replace('_ADD', '')
            else: cleanFileName = fileName.replace('.pdf', '').replace('_ADD', '')
            if condenseList.count(cleanFileName) == 0: 
                condenseList.append(cleanFileName)
                repFiles[0].append(cleanFileName)
                repFiles[1].append(stringContents.count(cleanFileName))
                repFiles[2].append(cleanFileName + '.pdf')
                repFiles[3].append(0)
                repFiles[4].append('')    
            repFiles[0].append(cleanFileName)
            repFiles[1].append(stringContents.count(cleanFileName))
            repFiles[2].append(fileName)
            priorCount = repFiles[0].count(cleanFileName)
            repFiles[3].append(priorCount)
            repFiles[4].append('')
            # repFiles[3].append(eval(str(fileName[fileName.rfind("(")+1:fileName.rfind(")")]).lstrip('0')))
    
    # for it in condenseList: print it
    '''
    print '**---'
    print repFiles[0][0]  # clean file name
    print repFiles[1][0]  # count of files with same name
    print repFiles[2][0]  # filename
    print repFiles[3][0]  # index number of repeat
    print repFiles[4][0]  # number of pages
    print '--**'
    '''

    # return
    repFile = condenseList[0]
    for repFile in condenseList:
        print repFile
        print 'repCount=', repFiles[0].count(repFile)
        if TEST == True: return   
        pt = 0
        for i in range(0, repFiles[0].count(repFile)):
            pt = repFiles[0].index(repFile, pt)
            filePath = FileStartDir[1:].replace("/", ":") + ':' + repFiles[2][pt]
            # print filePath
            openPDF(filePath)
            repFiles[4][pt] = getPageCount()
            closeFileWindow(repFiles[2][i])
            pt += 1
    
        redFiles = []
        redPages = 0
        redList = [], [], []
        fileSet = 0
        pages = 0
        iterCnt = repFiles[0].count(repFile)
        pt = 0
        for k in range(0, iterCnt):
            pt = repFiles[0].index(repFile, pt)
            pages = pages + eval(str(repFiles[4][pt]))
            # print pages
            redFiles.append(repFiles[2][pt])
            if pages >= 100 or k == iterCnt - 1:
                redList[0].append(str(fileSet))
                redList[1].append(redFiles)
                redList[2].append(str(pages))
                redFiles = []
                pages = 0
                fileSet = fileSet + 1
            pt += 1
        ''' 
        for i in range(0,len(redList[0])):
            print i,redList[0][i]
            print i,redList[1][i]
            print i,redList[2][i]
        print redList
        '''
        print '........'
        moveFiles = []
        for m in range(0, len(redList[0])):
            filePath = FileStartDir[1:].replace("/", ":") + ':' + redList[1][m][0]
            print 'openfile', filePath
            moveFiles.append(redList[1][m][0])
            openPDF(filePath)
            for j in range(1, len(redList[1][m])):
                addFilePath = FileStartDir[1:].replace("/", ":") + ':' + redList[1][m][j]
                print 'addFile', addFilePath
                moveFiles.append(redList[1][m][j])
                pageIndex = getPageCount() - 1
                cleanFilePath = ("/" + addFilePath).replace(':', '/')
                if TEST == False: insertAllPages(pageIndex, cleanFilePath)
            newName = repFile + '_AGGR_(' + str(eval(redList[0][m]) + 1) + ')' + '.pdf'
            fileSave = FileStartDir[1:].replace("/", ":") + ':' + newName
            cleanFilePath = ("/" + fileSave).replace(':', '/')
            print 'savePath', cleanFilePath  
            if TEST == False: renamePDF(cleanFilePath)
            if TEST == False: closeFileWindow(newName)
            if TEST == True: closeFileWindow(filePath)
        print ''
        for it in moveFiles:
            cmd = 'mv "' + FileStartDir + '/' + it + '" "' + FileEndDir + '/' + it + '"'
            print cmd
            if TEST == False: system(cmd)
        print '........'
    ''' 
            if len(redList[1][m]) > 1:
                for n in range(1,len(redList[1][m])):
                    pageIndex=getPageCount()-1
                    addFilePath = FileStartDir[1:].replace("/",":") +':'+redList[1][m][n]
                    cleanFilePath = ("/"+addFilePath).replace(':','/')
                    insertAllPages(pageIndex,cleanFilePath)
                   
            newName = condenseList[0]+'_Aggr_'+str(eval(redList[0][m])+1)+'.pdf'
            fileSave = FileEndDir[1:].replace("/",":") +':'+newName
            cleanFilePath = ("/"+fileSave).replace(':','/')
            renamePDF(cleanFilePath)
            closeFileWindow(newName)
    
        print 'completed aggregation'
    '''

def makeHTMLIndex(startDir, endFileName='index.html', htmlTitle='', cols=''):
    endFilePath = startDir + endFileName
    x = getFilesFolders(startDir)

    dates, titles, links = [], [], []
    a = HTML_API.addTag('b', 'Date')
    b = HTML_API.addTag('b', 'Title')
    list_data, list_options = [], []
    list_data.append([a, b])
    list_options.append(['', ''])

    for it in x:
        listVar, list_option_var = [], []
        if cols.count('date') != 0:
            d = it[:it.find(' ')]
            if d == '0000.00.00': listVar.append('---')
            elif d.find('.00.') != -1: date = d[:4]
            elif d[-3:] == '.00': listVar.append(custom_strings.change_date(d[:-3], 'Y.m', 'b-Y'))
            else:  listVar.append(custom_strings.change_date(d, 'Y.m.d', 'd-b-Y'))  # 'Y.m.d','dd-b-Y'
            list_option_var.append('align="right"')
        # date=HTML_API.addTag('p',date,'align="right"')
        # print date

        title = it[it.rfind('/') + 1:]
        if title.find('_OCR') != -1: title = title.replace('_OCR', '')
        link = HTML_API.hyperlink(title, it.replace(startDir, ''))
        print link
        print sad
        listVar.append(link)
        
        list_option_var.append('')
        
        list_data.append(listVar)  
        list_options.append(list_option_var)
        
    table1 = HTML_API.addTag('div', HTML_API.makeTableFromList(list_data, list_options, '750'), 'align="center"')
    
    # table2_header=HTML_API.addTag('div',HTML_API.addTag('h2','Additional Related Archival Documents'))
    # startDir="/Users/admin/Desktop/Bayh-Dole/3_DIV_SCAN"
    # x=getFilesFolders(startDir)
    # list_data,list_options=[],[]
    # for i in range(0,len(x)):
    #    it=x[i]
    #    list_data.append(HTML_API.hyperlink('Archival Supp. '+str(i+1),startDir+'/'+it))
    # table2=HTML_API.addTag('div',HTML_API.makeListFromList(list_data))
    
    html = HTML_API.makeHTML(table1, "htmlTitle")
    f = open(endFilePath, 'w')
    f.write(html)
    f.close()

def limitFilesFromHTML():
    FromDir = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/JGpdfs"
    ToDir = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/strict"
    sourceFile = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/JG_index.html"

    f = open(sourceFile, 'r')
    x = f.read()
    f.close()

    linkCount = x.count("href=")

    fileList = []
    pt = 0
    for i in range(0, linkCount):
        begin = x[pt:].find("href=") + 6 + pt
        pt = begin + 1
        end = x[pt:].find('"') + pt
        pt = end + 1
        fileName = x[begin + 7:pt - 1]
        fileList.append(fileName)
        # fileOSPath = FromDir+'/'+fileName
        # fileOSDest = ToDir+'/'+fileName
        # system("cp '"+fileOSPath+"' '"+fileOSDest+"'")

    newFileList = listdir(ToDir)
    # exclude = [".DS_Store"]
    # exclude.extend(ToDir)
    for item in newFileList:
        try:
            fileList.remove(item)
        except:
            if item != '.DS_Store':
                fileOSPath = FromDir + '/' + item
                fileOSDest = ToDir + '/' + item
                system("cp '" + fileOSPath + "' '" + fileOSDest + "'")
            print item
    # print fileList


def touchUpHTML(sourceFile, savePath):
    # FromDir = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/JGpdfs"
    # ToDir = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/strict"
    # sourceFile = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/JG_index.html"
    # sourceFile2 = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/JG_index2.html"

    f = open(sourceFile, 'r')
    x = f.read()
    f.close()

   # links=HTML_API.getAllTag(x,'a')
   # for it in links:
   #     a.append(it.get('href'))
   # print type(a[0]),a[0]
   # print asda

    linkCount = x.count("href=")

    folderPath, fileNames = [], []
    pt = 0
    for i in range(0, linkCount):
        begin = x.find("href=", pt) + 6
        pt = begin + 1
        end = x.find('"', pt)
        pt = end + 1
        f_path = x[begin:end]
        folderPath.append(f_path[:f_path.rfind('/') + 1])
        fileNames.append(f_path[f_path.rfind('/') + 1:])

    newFileNames = []
    for j in range(0, len(fileNames)):
        if fileNames[j].count(" ") != 0 or fileNames[j].count("-") != 0:
            newFileNames.append(fileNames[j].replace(" - ", "_").replace("-", "").replace(" ", "_").replace("__", "_"))
        else:
            newFileNames.append(fileNames[j])

    html = x
    html = html.replace('/Users/admin/Desktop/Bayh-Dole', '..')
    for k in range(0, len(fileNames)):
        # --#replace html
        html = html.replace(fileNames[k], newFileNames[k])
        # --#change files
        # fileOSPath = folderPath[k]+fileNames[k]
        # fileOSDest = folderPath[k]+newFileNames[k]
        # cmd="mv '"+fileOSPath+"' '"+fileOSDest+"'"
        # print cmd
        # system("mv '"+fileOSPath+"' '"+fileOSDest+"'")
    
    # endPT = html.find("Miscellaneous Undated Docs")
    # htmlEdit=html[:endPT]

    # htmlEdit = htmlEdit.replace("(1)</td>","").replace("(2)</td>","").replace("(3)</td>","")
    # htmlEdit = htmlEdit.replace("(4)</td>","").replace("(5)</td>","").replace("(7)</td>","")

    # newHTML = htmlEdit+html[endPT:]

    f = open(savePath, 'w+')
    f.write(html)
    f.close()

    print "done"
    

def adjustTitles():
    FromDir = "/Users/admin/Work/ScanBusiness/Dropbox/Scripts/sanspaper/scans"
    ToDir = "/Users/admin/Work/ScanBusiness/Dropbox/Scripts/sanspaper/files"
    sourceFile = "/Users/admin/Work/ScanBusiness/Dropbox/Scripts/sanspaper/BayhDole_index.html"
    sourceFile2 = "/Users/admin/Desktop/JerryGreenbergData/JerryGreenberg/BayhDole_index2.html"

    f = open(sourceFile2, 'r')
    x = f.read()
    f.close()

    linkCount = x.count("href=")

    fileList = []
    pt = 0
    for i in range(0, linkCount):
        linkRef = x.find("href=", pt)
        end1 = x.rindex("</td>", pt, linkRef)
        end = x.rindex("</td>", pt, end1 - 1)
        begin = x.rindex("<td>", pt, end) + 4
        pt = linkRef + 1
        fileName = x[begin:end]
        fileList.append(fileName)
        if fileName[0].isdigit() == True:
            print "fix this date: ", fileName

    cleanList = [("Def", "Defendants"),
              ("Memo", "Memorandum"),
              ("Aff", "Affirmation"),
              ("Pla", "Plaintiffs"),
              ("Resp", "Response"),
              ("SJ", "Summary Judgment"),
              ("Prod", "Production"),
              ("Req", "Request"),
              ("1st", "First"),
              ("Docs", "Documents"),
              ("Doc", "Document"),
              ("w", "with"),
              ("re", "regard"),
              ("convo", "conversation"),
              ("Opp", "Opposition"),
              ("Arg", "Argument"),
              ("Supp", "Support"),
              ("Cr-Motion", "Cross-Motion"),
              ("Dep", "Deposition"),
              ("Pla_Appellants", "Plaintiffs_Appellants"),
              ("Pla_Appellant", "Plaintiffs_Appellants"),
              ("Def_Appellees", "Defendants_Appellees"),
              ("Def_Appellants", "Defendants_Appellants"),
              ("en", "En"), ("banc", "Banc"),
              ("Dist", "District"),
              ("pg", "page"), ("wo", "without"), ("w", "with"),
              ("Appelants", "Appellants")]
    caseSpecific = [("Curae", "Curiae"),
               ("infriinged", "infringed"),
               ("Phot", "Photo"),
               ("dos", "documents"),
               ("Exerpts", "Excerpts"),
                  ("Keny", "Kent"),
                  ("Appropiate", "Appropriate"),
                  ("Accomp", "Accompanying"),
                  ("Seahawk", "SeaHawk"),
                  ("Permenant", "Permanent"),
                  ("Yello", "Yellow"),
                  ("Assaul", "Assault")]
    cleanList.extend(caseSpecific)

    oldWord, newWord = [], []
    for pair in cleanList:
        oldWord.append(pair[0])
        newWord.append(pair[1])
        
    newList = []
    totalWordList = []
    for j in range(0, len(fileList)):
        wordGroup = fileList[j].split()
        newGroup = ""
        for k in wordGroup:
            if oldWord.count(k.lower().capitalize()) != 0:
                newGroup = newGroup + newWord[oldWord.index(k.lower().capitalize())] + " "
            elif oldWord.count(k) != 0:
                newGroup = newGroup + newWord[oldWord.index(k)] + " "
            else:
                newGroup = newGroup + k + " "
    # #            if totalWordList.count(k) == 0:
    # #                totalWordList.append(k)
        if newGroup[0].islower() == True:
            newGroup = newGroup[0].upper() + newGroup[1:]
        newList.append(newGroup)

    print len(newList), " should equal ", len(fileList)

    html = x[:]
    for k in range(0, len(fileList)):
        # --#replace html
        html = html.replace(fileList[k], newList[k])

    f = open(sourceFile2, 'w+')
    f.write(html)
    f.close()

    print "done"
    # make classes

    # consolidateReps()
    # runSpeedDivide()
    # runPageCount()
    # limitFilesFromHTML()
    # touchUpHTML()


if __name__ == '__main__':
    orig_folder = "Users:sethchase:Work:ScanBusiness:Clients:UNH:Bayh-Dole:0_ORIG"
    get_folder = "Users:sethchase:Work:ScanBusiness:Clients:UNH:Bayh-Dole:2_OCR"
    put_folder = "Users:sethchase:Work:ScanBusiness:Clients:UNH:Bayh-Dole:3_DIV_SCAN:"
    DIVIDER_words = ['NEXT', 'DOUBLE']
    labels = ['NEXT', 'DBL']
    
    startDir = "/Users/admin/Desktop/Bayh-Dole/4_PREPPED_FILES"
    endDir = "/Users/admin/Desktop/Bayh-Dole/4_PREPPED_FILES/parts"
    HTMLpath1 = '/Users/admin/Desktop/Bayh-Dole/HTML/Bayh-Dole1.html'
    HTMLpath2 = '/Users/admin/Desktop/Bayh-Dole/HTML/Bayh-Dole2.html'
    
    try:
        cmd = []
        for i in range(1, len(argv)): cmd.append(argv[i])
        if len(cmd) == 1: cmd.append(getcwd() + '/')
        elif cmd[1].find('/') == -1: cmd[1] = getcwd() + '/' + cmd[1]
        # print cmd
        stop = False
    except:
        cmd = ['']
        pass
        # print 'argument error (or testing)'
        # username,password,command='','',''
        stop = True

    if cmd == []: pass
    else:
        print len(cmd)
        print cmd[1]
        if cmd[0] == 'run':  runSpeedDivide()
        elif cmd[0] == 'runPageCount':  runPageCount(cmd[1])
        elif cmd[0] == 'runFolderCount':  runFolderCount(cmd[1])
        elif cmd[0] == 'runCopyDocs':  runCopyDocs(cmd[1])
        elif cmd[0] == 'runUpdateDocs':  runUpdateDocs(cmd[1])
        elif cmd[0] == 'CopyFilesToExcel':  CopyFilesToExcel(cmd[1])
        elif cmd[0] == 'consolidateReps':  consolidateReps(startDir, endDir) 
        elif cmd[0] == 'makeHTMLIndex':  # (startDir,endFileName='index.html',htmlTitle='',cols='')
            if len(cmd) == 2: makeHTMLIndex(cmd[1]) 
            elif len(cmd) == 3: makeHTMLIndex(cmd[1], cmd[2]) 
        elif cmd[0] == 'limitFilesFromHTML':  limitFilesFromHTML(cmd[1])
        elif cmd[0] == 'touchUpHTML':  touchUpHTML(HTMLpath1, HTMLpath2)
        elif cmd[0] == 'adjustTitles':  adjustTitles(cmd[1])
        elif cmd[0] == 'DivideByPageContent':  DivideByPageContent(cmd[1])
        
    # startDir = "/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/4_PREPPED_FILES"
    # startDir,endDir
    
    # workDir='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR/'
    # folder=listdir(workDir)
    # if folder.count('.DS_Store') != 0: folder.pop(folder.index('.DS_Store'))
    
    # reOCRwithRotation(folder)
    # combinePDFSupps()
    # DivideByPageContent(orig_folder,get_folder,put_folder,DIVIDER_words,labels)


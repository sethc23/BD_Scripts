# import sortListArray,listFout,listFin
# from appscript import *
# import os, osax
# from datetime import date
# import SpeedDividePDF
# from SpeedDividePDF import *  # combinePDFSupps

import os, time
from datetime import datetime
import subprocess
#import commands
from sys import argv, path
# path.append('/Users/admin/SERVER2/BD_Scripts/utility')
#path.append('/Users/admin/SERVER2/BD_Scripts/law')
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
# from Adobe_API import getFolderPDFCount, openPDF, closePDF
# from Adobe_API import renamePDF, deletePages, savePDF, openFile, insertPages
# from Adobe_API import getPageCount, zipSinglePDF, extract_delete
# from Adobe_API import reversePDF, getPageCount, runPageOCR
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from HTML_API import html_space, addTag, horizontalRule
from HTML_API import makeTableRowsFromFilePaths, makeTableFromRows, getAllTag
import os


def exec_cmd(cmd):
    from os import system
    if system(cmd) != 0:
        print 'error with cmd',cmd
        raise SystemExit

def getCapsLock():
    p = os.popen('xset q | grep LED')
    s = p.read()
    p.close()
    x = s[65]
    if x == '0': return 'off'
    if x == '1': return 'on'

def cleanFilePaths(file_or_files):
    invalid_char = [' ', '|', ',', '&', '(', ')', "'"]
    if type(file_or_files) == str: 
        string = True
        file_or_files = [file_or_files]
    for i in range(0, len(file_or_files)):
        filePath = file_or_files[i]
        for it in invalid_char:
            if filePath.find(it) != -1: file_or_files[i] = file_or_files[i].replace(it, '\\' + it)
        # if filePath[len(filePath)-1] != '/': 
        #    file_or_files[i]=file_or_files[i]+'/'
    if string == True: return file_or_files[0]
    else: return file_or_files 

def click(spot=""):
    if spot == "":
        spot=str(getMouseSpot()).replace(" ","").strip("()").split(',')
    os.system('/usr/bin/cliclick '+spot[0]+' '+spot[1])

def beep():
    cmd='say -v Bells "dong"'
    exec_cmd(cmd)

def getMouseSpot():
    p = os.popen('/usr/bin/cliclick -q')
    s = p.read()
    p.close()
    x, y = s.split(',')
    x = eval(x.strip())
    y = eval(y.strip())
    return x, y

def get_input(question):
    return raw_input(question)
    

def syncPreferenceFiles(prefFilePath):
    f = open(prefFilePath, "r")
    x = f.readlines()
    f.close()
    A, B = x[0].lstrip('\n').rstrip('\n'), x[1].lstrip('\n').rstrip('\n')
    if checkFilePathExists(A) == False or checkFilePathExists(B) == False:
        print "error: base sync folders are unavailable"
        return
    syncFiles = []
    for i in range(3, len(x)): syncFiles.append(x[i].lstrip('\n').rstrip('\n'))
    for it in syncFiles:
        first = os.stat(A + it).st_mtime
        second = os.stat(B + it).st_mtime
        if first == second: pass
        else:
            if first > second: old, new = B, A
            else: old, new = A, B
            fromPath, toPath = new + it, old + it
            cmd = 'cp "' + fromPath + '" "' + toPath + '"'
            print cmd
            os.system(cmd)

def getProcesses():
    p = os.popen('ps -A')
    s = p.read()
    p.close()
    s = s.split('\n')
    return s

def checkFile(filePath):
    fileName = filePath[filePath.rfind('/') + 1:]
    fileDir = filePath[:filePath.rfind('/')]
    tempDir = os.getcwd() + '/'
    tempFolderInfo = tempDir + "temp.txt"
    print fileName
    print fileDir
    print tempDir
    print tempFolderInfo
    execCommand = "ls -l '" + fileDir + "' > " + tempFolderInfo
    os.system(execCommand)
    f = open(tempFolderInfo, "r")
    z = f.readlines()
    f.close()
    fileInfo = None
    for i in range(0, len(z)):
        if z[i].find(fileName) != -1:
            fileInfo = z[i]
            break
    if fileInfo != None:
        s = fileInfo.find(fileName) - 13
        timeModified = fileInfo[s:s + 12].strip() + " " + str(time.strftime("%y", time.localtime()))
        timeWas = time.strptime(timeModified, "%b %d %H:%M %y")
        epochTime = int(time.mktime(timeWas))
        now = time.time()
        whenChanged = int(now) - epochTime
        minutesAgo = int(whenChanged / 60.0)
        return minutesAgo
    else:
        return None

def checkFilePathExists(filePath):
    try:
        # open(filePath)
        if os.path.isfile(filePath): return True
        else: return False
    except:
        return False

def checkFolderPathExists(folderPath):
    try:
        # open(filePath)
        if os.path.isdir(folderPath): return True
        else: return False
    except:
        return False

def get_pwd():
    from os.path import dirname,realpath
    return dirname(realpath(__file__))

def getFileInfo(filePath,C_or_M="c"):
    x=os.path.getctime(filePath)
    y=datetime.fromtimestamp(x).strftime('%d%b%Y %H:%M:%S')
    return y

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_folder_sizes(start_path = '.'):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    z=os.getcwd()
    x=getAllFolders(z)
    for it in x: 
        a=get_size(it)
        print locale.format("%d",round(a/1000.0,0), grouping=True),'\t\t',it
        
def getAllFolders(workDir):
    x = os.listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    popList, y = [], []
    for i in range(0, len(x)):
        if os.path.isdir(x[i]): 
            y.append(workDir.rstrip('/')+'/'+x[i])
        else: y.append(workDir.rstrip('/')+'/'+x[i])
    return y

def getFilesFolders(workDir, full=False):
    x = os.listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    popList, y = [], []
    for i in range(0, len(x)):
        if os.path.isdir(x[i]): 
            popList.append(i)
        else: y.append(workDir.rstrip('/')+'/'+x[i])
    popList.reverse()
    for it in popList: x.pop(it)
    if full == False: return x
    else: 
        return y

def getAllFilePaths(workDir):
    folderPath,filePaths,nextPath,folders = workDir,[],[],[]
    contents = os.listdir(workDir)
    exclude_files = ['.DS_Store']
    exclude_extensions = []
    while len(contents) != 0:
        it = contents[0].strip('/')
        # print 'it',it
        newPath = folderPath.replace(workDir, '').strip('/') + '/' + it.strip('/')
        # print '--new',newPath
        checkPath = workDir + '/' + newPath.rstrip('/')
        # print '---folder+it',checkPath
        if exclude_files.count(it) != 0:
            contents.pop(0)
        elif checkFolderPathExists(checkPath):
            # print 'print folder',it
            nextPath.append(checkPath)
            contents.pop(0)
        elif checkFilePathExists(checkPath):
            filePaths.append(checkPath)
            contents.pop(0)
        else:
            print it
            print checkFolderPathExists(checkPath)
            print checkFilePathExists(checkPath)
            print checkPath
            print folderPath
            print 'shit!'
            raise SystemExit
        if len(contents) == 0:
            if len(nextPath) != 0:
                while nextPath != 0:
                    nextFolder = nextPath.pop(0)
                    contents = os.listdir(nextFolder)
                    if len(contents) == 1: contents.pop(0)
                    else:
                        folderPath = nextFolder.replace('//', '/')  # .lstrip('/')#[nextFolder.rfind('/'):].lstrip('/')
                        folders.append(folderPath)
                        # print folderPath
                        # print folderPath.replace(workDir,'')
                        break
    # print len(contents)
    # print asdsa
    return filePaths, folders

def get_files_in_selection():
    from appscript import app
    app(u'Finder').activate()
    files = app(u'Finder').selection.get()
    fileNames, fileTypes, filePaths = [], [], []
    
    try:
        for arg in argv:
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
    return fileNames, fileTypes, filePaths

def getFolderContents(workDir, clean=True, opt=''):  # clean=False includes ".DS_Store"
    fileList, folderCount, fileSizes, totalSize = [], 0, [], 0
    rootdir = workDir
    for root, subFolders, files in os.walk(rootdir):
        folderCount += len(subFolders)
        for file in files:
            f = os.path.join(root, file)
            if clean == True:
                if f.find('.DS_Store') != -1: f = ''
            if f != '':
                if opt.find('filesizes') != -1:
                    fileSizes.append(os.path.getsize(f))
                if opt.find('totalsize') != -1:
                    totalSize += os.path.getsize(f)
                fileList.append(f)            
    if opt != '':
        returnVars = []
        if opt.find('filesizes') != -1:
            returnVars.append(['filesizes', fileSizes])
        if opt.find('totalsize') != -1:
            returnVars.append(['totalsize', totalSize])
        return fileList, folderCount, returnVars
    else: return fileList, folderCount

def splitPath_filename(allPaths):
    filePaths, fileNames = [], []
    for it in allPaths:
        filePaths.append(it[:it.rfind('/') + 1])
        fileNames.append(it[it.rfind('/') + 1:])
    return filePaths, fileNames

def renameFileSet(workDir, label_1, label_2):
    # workDir='/Users/admin/Desktop/beat_dealer'
    allPaths = getAllFilePaths(workDir)
    filePaths, oldNames = splitPath_filename(allPaths)

    newNames, popList = [], []
    for i in range(0, len(oldNames)):
        it = oldNames[i]
        if it.find(label_1) != -1:
            newNames.append(it.replace(label_1, '').replace('.pdf', 'a.pdf'))
        elif it.find(label_2) != -1:
            newNames.append(it.replace(label_2, '').replace('.pdf', 'b.pdf'))
        else:
            popList.append(i)

    popList.reverse()
    for it in popList:
        oldNames.pop(it)

    if len(oldNames) == len(newNames):
        for i in range(0, len(newNames)):
            # renameFile(filePaths[i],oldNames[i],newNames[i])
            print oldNames[i]
            print newNames[i]
            break

def renameFileZ(filePath, oldName, newName, test=True):
    filePath = cleanFilePaths(filePath)
    oldName = cleanFilePaths(oldName)
    newName = cleanFilePaths(newName)
    if test == True:
        print 'old-- ', oldName
        print 'new-- ', newName
    cmd = 'mv ' + filePath + '/' + oldName + ' ' + filePath + '/' + newName
    if test == True: print cmd
    else: os.system(cmd)


def deleteFile(filePath, confirm=True):
    if confirm == True:
        check = raw_input("Do you want to delete the following file? (y/n)\n\n" + filePath + '\n')
        if check == 'y': os.remove(filePath)
        elif check == 'n': return
    else: os.remove(filePath)

def deleteFilesWithVar(workDir, del_var, inverse=False, confirm=True):
    x = getFilesFolders(workDir, full=True)
    for it in x:
        if inverse == True:  # meaning, delete everything EXCEPT filename with VAR
            if it.find(del_var) != -1: pass
            else:
                if confirm == True:
                    check = raw_input("Do you want to delete the following file? (y/n/ignore all)\n\n" + it + '\n')
                    if check == 'y': os.remove(it)
                    elif check == 'n': break
                    elif check == 'ignore all':  confirm = False
                else: os.remove(it)     
        else:
            if it.find(del_var) == -1: pass
            else:
                if confirm == True:
                    check = raw_input("Do you want to delete the following file? (y/n/ignore all)\n\n" + it + '\n')
                    if check == 'y': os.remove(it)
                    elif check == 'n': break
                    elif check == 'ignore all':  confirm = False 
                else: os.remove(it)

def findReplaceFileName(workDir, findVar, replaceVar, verbose=False):
    x = getFilesFolders(workDir, full=False)
    oldName, newName = [], []
    for fileName in x:
        if fileName.find(findVar) != -1:
            oldName.append(workDir + fileName)
            newName.append(workDir + fileName.replace(findVar, replaceVar))
    for i in range(0, len(oldName)):
        if verbose != False: print oldName[i], newName[i]
        cmd = 'mv ' + oldName[i] + ' ' + newName[i]
        os.system(cmd)
        

def copy(txt):
    # txt=unicode(txt).encode('ascii','replace')
    os.system('echo "' + txt + '" | pbcopy')

def getClipboardData():
    # p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    # retcode = p.wait()
    # data = p.stdout.read()
    # return data
    # txt=unicode(txt).encode('ascii','replace')
    p = os.popen('pbpaste')
    s = p.read()
    p.close()
    return s

def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

def getPageCounts(workDir):
    '''
    workDir0='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
    workDir1='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
    workDir2='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR'
    workDir3='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR/OCR1'
    put_folder='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
    
    workDir=workDir3
    '''
    folder, popList = os.listdir(workDir), ['.DS_Store']
    for it in folder:
        if it.lower().find('.pdf') == -1: popList.append(it)
    for it in popList:
        if folder.count(it) != 0: folder.pop(folder.index(it))
    '''
    for it in folder:
        if it.find('.pdf') == -1:
            print 'ERROR'
            print it
            print asdasdfsa
    '''
    filePaths = []
    for it in folder:
        filePaths.append(workDir + '/' + it)
    print '\n' + workDir + '\n'
    fileNames, pgCounts = getFolderPDFCount(filePaths)
    for i in range(0, len(fileNames)):
        print fileNames[i] + '\t' + str(pgCounts[i])

def changeFileNames():
    workDir0 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
    workDir1 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
    workDir2 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR'
    
    workDir0 = '/Users/admin/Dropbox/BD_2012-Spring/Securities_Reg'
    workDir1 = '/Users/admin/next'
    workDir2 = '/Users/admin/'
    put_folder = '/Users/admin/Dropbox/BD_2012-Spring/Securities_Reg'
    
    workDirA = workDir0
    workDirB = workDir2
    
    folderA = os.listdir(workDirA)
    # folderB=os.listdir(workDirB)
    
    popList = ['.DS_Store', 'Slides', 'cases', 'z-alt_versions', 'agency_report']
    for it in popList:
        if folderA.count(it) != 0: folderA.pop(folderA.index(it))
    
    files1, files2 = [], []
    
    for it in folderA:
        filename1 = it
        files1.append(filename1)
        filename2 = filename1.replace('4-Class', '3-Class')
        files2.append(filename2)
    
    print len(files1), len(files2)
    
    for i in range(0, len(files1)):
        fromPath = workDir0 + '/' + files1[i]
        toPath = put_folder + '/' + files2[i]
        print 'fromPath', fromPath
        print 'toPath  ', toPath
        # break
        os.system('mv "' + fromPath + '" "' + toPath + '"')
        # if checkFileExists(toPath) == False: os.system('mv '+fromPath+' '+toPath)
        # else: print 'check',toPath


def decryptPDF_file(filePath):
    cmd = "guapdf -y -m " + filePath
    # print cmd
    os.system(cmd)
def decryptPDF_folder(folderPath):
    x = getFilesFolders(folderPath, full=True)
    for it in x:
        if it.find("decrypted") != -1: pass
        else:
            decryptPDF_file(it)

def pdfPageCount(filePath):
    from PyPDF2.pdf import PdfFileReader
    pdf = PdfFileReader(open(filePath))
    s=pdf.getNumPages()
    return s

def reducePDF_file(filePath):
    fileToPath = filePath.replace('.pdf', '_reduced.pdf')
    cmd = 'gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dPDFSETTINGS=/ebook -sOutputFile="' + fileToPath + '" "' + filePath + '"'
    # cmd='gs -sDEVICE=pdfwrite -dNOPAUSE -dNODISPLAY -dQUIET -dBATCH -dPDFSETTINGS=/ebook -sOutputFile="'+fileToPath+'" "'+filePath+'"'
    #print cmd
    #print asdfsd
    os.system(cmd)

def splitPDF(filePath,parts):
    pages=pdfPageCount(filePath)
    segs=int(pages)/int(parts)
    for i in range(0,parts):
        fileToPath = filePath.replace('.pdf', '_'+str(i+1)+'.pdf')
        cmd = 'gs -sDEVICE=pdfwrite -q -dNOPAUSE -dBATCH  -dFirstPage='+str((i*segs)+1)+' -dLastPage='+str((i+1)*segs)+' -sOutputFile="' + fileToPath + '" "' + filePath + '"'
        os.system(cmd)
    if pages > segs*parts:
        fileToPath = filePath.replace('.pdf', '_'+str(parts+1)+'.pdf')
        cmd = 'gs -sDEVICE=pdfwrite -q -dNOPAUSE -dBATCH  -dFirstPage='+str((segs*parts)+1)+' -dLastPage='+str(pages)+' -sOutputFile="' + fileToPath + '" "' + filePath + '"'
        os.system(cmd)

def reducePDF_folder(folderPath):
    x = getFilesFolders(folderPath, full=True)
    for it in x:
        reducePDF_file(it)    

def combinePDFSupps(get_folder, supp_folder="parts_combined"):
    # get_folder="/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR"
    put_folder = get_folder + supp_folder
    if os.path.exists(put_folder): pass
    else: os.system('mkdir "' + put_folder + '"')
    workDir1 = get_folder.rstrip('/')
    '''
    find partial files
    copy partial files to other folder
    '''
    x = os.listdir(workDir1)
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
                
    # print fileList[0]
    # print fileUnit[0]
    # add part 2 to part 1, move part 2 to another folder
    # '''
    combined = []
    for it in fileList:
        z = it.split('_')[1]
        # origFileName=z+'_001'
        origFileName = it.replace('_' + z, '_001') + '.pdf'  # it.split('_')[0]+'_'+it.split('_')[1],it.split('_')[0]+'_001')
        javaPath = workDir1 + '/' + origFileName
        
        # '''
        # print javaPath
        
        openFile(javaPath)
        lastPg = getPageCount() - 1
        pageIndex, sourceStart, sourceEnd = lastPg, None, None
        insert_vars = pageIndex, sourceStart, sourceEnd
        print 'adding:', workDir1 + '/' + it
        insertPages(workDir1 + '/' + it, insert_vars)
        javaPath = put_folder + '/' + it
        savePDF()
        closePDF()
        # '''
        fromPath = workDir1 + '/' + it
        toPath = put_folder + '/' + it
        # print 'fromPath',fromPath
        # print 'toPath  ',toPath
        if checkFilePathExists(toPath) == False: os.system('mv ' + fromPath + ' ' + toPath)
        else: print 'check', toPath        
        # break
    # '''


def moveOCRfiles():
    # are any files in workDir1 also in workDir2?  if so, move dupes to put_folder
    workDir2 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
    workDir1 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR'
    put_folder = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN/add'
    folder1 = os.listdir(workDir1)
    folder2 = os.listdir(workDir2)
    popList = ['1_unzipped', '.DS_Store', 'ORIG1']
    for it in popList:
        if folder1.count(it) != 0: folder1.pop(folder1.index(it))
        if folder2.count(it) != 0: folder2.pop(folder2.index(it))
    
    ct, ct1, ct2 = 0, 0, 0
    repeat = False
    sample = ''
    # print 'test',len(folder1),len(folder2)
    for it in folder1:
        # fileName2=it
        # fileName2=it[:-4]+'_OCR'+it[-4:]
        fileName2 = it.replace('_OCR', '')
        # fileName2=it[it.rfind('/')+1:].replace('_OCR','')
        # fileName2=it
        # print it
        # print fileName2
        # break
       
        if folder2.count(fileName2) != 0:
        # if folder2.count(fileName2) == 0:
            if sample == '':  sample = fileName2
            fromPath = workDir1 + '/' + it
            toPath = put_folder + '/' + it
            print 'fromPath', fromPath
            print 'toPath  ', toPath
            ct += 1
            # break
            if checkFilePathExists(toPath) != False: 
                # print '------- OVERRIGHT'
                 ct1 += 1
            else: 
                ct2 += 1
                '''
                if repeat==False:
                    print ""
                    print 'Move File? y/n/all'
                    print ""
                    choice = raw_input("")
                    print ""
                    #sleep(.25)
                    if choice == "y": 
                        os.system('mv '+fromPath+' '+toPath)
                        pass
                    elif choice == 'all': repeat=True
                    else: break
                elif repeat==True: 
                    os.system('mv '+fromPath+' '+toPath)
                    pass
                '''

            # else: print 'check',toPath
        # if folder2.count(it) != 0:
        #    #print it
        #    ct1+=1
    print ''
    print 'Are any files in:\n\t' + workDir1 + '\n  also in:\n\t' + workDir2 + '\n    ?'
    print ''
    print 'sample file:', sample, '\n'
    print 'total files:', ct
    print 'files moved:', ct2
    print '--- From folder:', workDir1
    print '--- To folder:', put_folder
    print 'files overwritten:', ct1

def runPDFzip():

    workDir0 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
    workDir1 = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/3_DIV_SCAN'
    workDir2 = '/Users/admin/Desktop/Divs/div'
    put_folder = '/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
    workDirA = workDir1
    workDirB = workDir2
    
    folderA = os.listdir(workDirA)
    # folderB=os.listdir(workDirB)
    files = []
    if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
    for it in folderA: 
        if it.find('DBL') != -1: 
            if it.find('ZIP') == -1: files.append(it)
    print len(files)
    for i in range(0, len(files)):
        fromPath = workDirA + '/' + files[i]
        openPDF(fromPath)
        pgCount = getPageCount()
        if len(str(float(pgCount) / 2)[str(float(pgCount) / 2).rfind('.') + 1:].replace('0', '')) != 0:
            label = 'DBL_ODD'
        else:
            label = "DBL_ZIP"
            zipSinglePDF()
        newPath = workDirA + '/' + files[i].replace('DBL', label)
        # renamePDF(newPath)
        # closePDF()
        toPath = put_folder + '/' + files[i]
        print ''
        print 'fromPath', fromPath
        print 'newPath', newPath
        print 'toPath  ', toPath
        print '--'
        # if checkFileExists(toPath) == False: os.system('mv '+fromPath+' '+toPath)
        # else: print 'check',toPath
        break

def zipPDF_File(filePath):
    print filePath
    x = zipSinglePDF(filePath)
    if x == 'success': pass
    else: print 'error zipping file', filePath
        
def zipPDF_Folder(folderPath):
    folderPath = folderPath.rstrip('/')
    # folderPath='/Users/admin/Desktop/wills'
    folderA = os.listdir(folderPath)
    if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
    for i in range(0, len(folderA)):
        filePath = folderPath + '/' + folderA[i]
        x = zipSinglePDF(filePath)
        if x == 'success': pass
        else: print 'error zipping file', filePath
        # openPDF(fromPath)
        # zipSinglePDF()
        # saveCurrent(fromPath)
        # closePDF()


def pgCt(filePath):
    print getPageCount(filePath)
def pgCtDir(folderPath):
    print 'teset'
    folderPath = folderPath.rstrip('/')
    # folderPath='/Users/admin/Desktop/wills'
    folderA = os.listdir(folderPath)
    if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
    ct = 0
    for i in range(0, len(folderA)):
        filePath = folderPath + '/' + folderA[i]
        openPDF(filePath)
        x = getPageCount()
        ct += eval(str(x))
        closePDF() 
    print ct

def folderOCR(folderPath):
    import datetime, time
    folderPath = folderPath.rstrip('/')
    # folderPath='/Users/admin/Desktop/wills'
    folderA = os.listdir(folderPath)
    if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
    for i in range(0, len(folderA)):
        filePath = folderPath + '/' + folderA[i]
        openPDF(filePath)
        runPageOCR()
        closePDF()   

def scrap(folderPath):
    fromDir = '/Users/admin/Desktop/combine'
    fromFiles = os.listdir(fromDir)
    if fromFiles.count('.DS_Store') != 0: fromFiles.pop(fromFiles.index('.DS_Store'))
    # toFiles=[]
    # for i in range(0,len(fromFiles)): toFiles.append(filter(lambda x: x.isdigit(), fromFiles[i]))
    # f=True
    for i in range(0, len(fromFiles)): 
        fromV = fromDir + '/' + fromFiles[i]
        old = fromFiles[i][:fromFiles[i].rfind('_')]
        toFileName = fromFiles[i].replace(old, '0395')
        toV = fromDir + '/' + toFileName
        # if f==True:
        #    f=False
        #    toV=toV.replace(toFiles[i],'001')
        # print fromV
        # print toV
        #  0689_001.pdf

        # renameFileZ(toDir,toFiles[i],fromFiles[i])
        cmd = 'mv ' + fromV + ' ' + toV
        # print cmd
        os.system(cmd)
        # break


def scrap2(folderPath):
    workDir = '/Users/admin/Desktop/Hennessey/contents'
    filePaths, folderCount = getFolderContents(workDir, clean=True, opt='')
    
    for it in filePaths:
        fol_path = it[:it.rfind('/')]
        item_name = it[it.rfind('/') + 1:]
        invalid_char = [' ', '|', ',', '&', '(', ')', "'"]
        for char in invalid_char:
            if it.find(char) != -1:
                renameFileZ(fol_path, item_name, item_name.replace(char, '_'))
                it = it.replace(char, '_')
    allFiles = []
    for it in filePaths: allFiles.append(it[it.rfind('/') + 1:])

    fpath = '/Users/admin/Desktop/Hennessey/index_v1.txt'
    f = open(fpath, 'r')
    x = f.read()
    f.close()
    print 'number of files reviewed (including folders)', len(x.split('\r'))
    print 'number of folders', folderCount
    print 'number of files reviewed (NOT including folders)', len(x.split('\r')) - folderCount
    opt, reviewFilePaths = [], []
    for i in range(0, len(x.split('\r'))):
        row = x.split('\r')[i].split('\t')
        tempRow = ''
        for j in range(1, len(row)):
            tempRow += row[j]
        try:
            all_index = allFiles.index(tempRow)
            reviewFilePaths.append(allFiles[all_index])
            opt.append(row[0])
        except:
            pass
            # print tempRow

    print 'number of options', len(opt)
    print 'number of reviewFiles', len(reviewFilePaths)
    print filePaths[0]
    html_table_rows = makeTableRowsFromFilePaths(workDir, filePaths)
    
    print len(filePaths), len(html_table_rows)
    for i in range(0, len(html_table_rows)):
        row = html_table_rows[i]
        # print row
        rowData = getAllTag(row, 'td')[0].strip('/')
        rowData = rowData.replace(html_space(), '')
        rowFile = getAllTag(rowData, 'a')
        try:
            rowFile = rowFile[0]
        except:
            rowFile = ''
        # rowOption=
        # print rowData
        # print adsa
       # print reviewFilePaths.count(rowData),rowData
        if reviewFilePaths.count(rowFile) != 0:  # if data has an option...
            # new col with option
            # print 'option'
            rev_ind = reviewFilePaths.index(rowFile)
            if opt[rev_ind] == '': review_option = html_space()
            else: review_option = opt[rev_ind]
            newRow = addTag('td', review_option, 'class="td_1"') + row
        else:
            # new col with space
            newRow = addTag('td', html_space(), 'class="td_1"') + row
        html_table_rows[i] = newRow
        # print asds
    
    
    
    billWork_html, billFile_html, remainder_html = [], [], []
    for it in html_table_rows:
        # print it
        if it.find('f_1') != -1:
            billWork_html.append(it)
            billFile_html.append(it)
            remainder_html.append(it)
        else:
            # rowData=getAllTag(it,'td')
            rowData = getAllTag(it, 'td')[0]
            # print rowData
            # print dsda
            # rowData=rowData.replace(html_space(),'')
            # rowData=getAllTag(rowData,'a')
            # print rowData
            option = rowData
            # print option
            if option == 'a': billWork_html.append(it)
            elif option == 'b': billFile_html.append(it)
            else: remainder_html.append(it)
        # print asdsa
        # if it

    html_body = horizontalRule()
    # html_body+=makeTableFromRows(html_table_rows,width='700px')  
    # '''
    html_body += addTag('h1', 'Works by Bill Hennessey: (may have some errors and need to verify)') + horizontalRule()
    html_body += makeTableFromRows(billWork_html, width='700px')
    html_body += addTag('h1', "Bill Hennessey's Files: (may have some errors and need to verify)") + horizontalRule()
    html_body += makeTableFromRows(billFile_html, width='700px')
    html_body += addTag('h1', "Files with Errors:") + horizontalRule()
    html_body += makeTableFromRows(remainder_html, width='700px')    
    # '''
    
    html_template = '/Users/admin/Desktop/Hennessey/Hennessey_Template.html'
    f = open(html_template, 'r')
    z = f.read()
    f.close()
    
    html = z.replace('#BODY#', html_body)
    
    f = open('/Users/admin/Desktop/Hennessey/Hennessey_index.html', 'w')
    f.write(html)
    f.close()
"""
    filePaths,folders=getAllFilePaths(workDir)
    a=filePaths
    #for it in a: print it
    #a.pop(0)
    #print fpath[0]
    #print x[:100]
    print len(fpath),len(x.split('\r')),len(a),len(opt)
    fnames2=[]
    for i in range(0,len(a)):
        fnames2.append(a[i][a[i].rfind('/')+1:])
    pt=0
    for i in range(0,len(a)):
        #last=fpath[i]
        if fpath.count(a[i]) != 0: pass
        else: 
            if checkFilePathExists(a[i]) == False:
                pt+=1
                print a[i]
    print pt
        #print x.split('\r')[i]
        #print a[i]
        #fpath=row[1]
        #if row[2]!='': fpath+='/'+row[2]
        #if row[3]!='': fpath+='/'+row[3]
"""     

def getFileFolderInfo(folderPath):
    pass


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
        #print len(cmd)
        if cmd[1] == 'getPageCounts':
            getPageCounts(cmd[2])
            #getPageCounts('/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN')
        elif cmd[1] == 'zipPDF_File': 
            print cmd[1]
            zipPDF_File(cmd[2])
        elif cmd[1] == 'zipPDF_Folder': zipPDF_Folder(cmd[0])
        elif cmd[1] == 'combinePDFparts':
            if len(cmd) == 2: combinePDFSupps(cmd[0])
            if len(cmd) == 3: combinePDFSupps(cmd[0],cmd[2])
        elif cmd[1] == 'changeFileNames': changeFileNames()
        elif cmd[1] == 'reversePDF': reversePDF(cmd[2])
        elif cmd[1] == 'pgct': pgCt(cmd[2],cmd[3])
        elif cmd[1] == 'pgctdir': pgCtDir(cmd[2])
        elif cmd[1] == 'folderOCR': folderOCR(cmd[2])
        elif cmd[1] == 'syncPrefs': syncPreferenceFiles(cmd[2])
        #elif cmd[1] == 'scrap': scrap(cmd[0])  ##  in this directory replace {1} with {2}     {1}="{'a','b'}"
        elif cmd[1] == 'scrap': scrap2(cmd[0]) 
        #elif cmd[1] == 'convertAudio': convertAudio(cmd[1],cmd[2])
        elif cmd[1] == 'getFolderSizes': get_folder_sizes()
        elif cmd[1] == 'splitPDF': splitPDF(cmd[2], cmd[3])
        elif cmd[1] == 'reducePDF_folder': reducePDF_folder(cmd[2])
        
"""    
        #folderPath='/Users/admin/Desktop/ethics'
        #folderA=os.listdir(folderPath)
        #if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
        
        #filePath='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/3_DIV_SCAN/2900_001_OCR_DBL_ODD_0.pdf'
        #print checkFilePathExists(filePath)
        workDir0='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/0_ORIG'
        workDir1='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/1_SCAN'
        #/1_unzipped
        workDir2='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/2_OCR'
        #/parts_combined
        workDir3='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/3_DIV_SCAN'
        workDir4='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/4_PREPPED_FILES'
        put_folder=workDir4
        workDirA=workDir1
        workDirB=workDir2
        
        x='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/4_PREPPED_FILES/1962.09.01 - Federal Bar Journal vol.22.n.4.pdf'
        extract_delete(1,10,x)
    
        folderA=os.listdir(workDirA)
        #folderB=os.listdir(workDirB)
        files=[]
        if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
        for it in folderA: 
            if it.find('DBL') != -1: 
                if it.find('ZIP') == -1: files.append(it)
        print len(files)
        for i in range(0,len(files)):
            fromPath=workDirA+'/'+files[i]
            openPDF(fromPath)
            pgCount=getPageCount()
            if len(str(float(pgCount)/2)[str(float(pgCount)/2).rfind('.')+1:].replace('0',''))!=0:
                label='DBL_ODD'
            else:
                label="DBL_ZIP"
                zipSinglePDF()
            newPath=workDirA+'/'+files[i].replace('DBL',label)
            #renamePDF(newPath)
            #closePDF()
            toPath=put_folder+'/'+files[i]
            print ''
            print 'fromPath',fromPath
            print 'newPath',newPath
            print 'toPath  ',toPath
            print '--'
            #if checkFileExists(toPath) == False: os.system('mv '+fromPath+' '+toPath)
            #else: print 'check',toPath
            break
    
        #changeFileNames()
        #moveOCRfiles()

"""
#splitPDF('/Users/admin/Desktop/9100KDEY.pdf', 10)
#reducePDF_folder('/Users/admin/Desktop/filing/')
#get_size_folders('/Users/admin/Dropbox')


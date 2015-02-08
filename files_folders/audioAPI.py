# import sortListArray,listFout,listFin
# from appscript import *
# import os, osax
# from datetime import date
# import SpeedDividePDF
# from SpeedDividePDF import *  # combinePDFSupps

import audiotools
import os
import subprocess
from sys import argv, path
# path.append('/Users/admin/SERVER2/BD_Scripts/utility')
path.append('/Users/admin/SERVER2/BD_Scripts/law')
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from Adobe_API import getFolderPDFCount, openPDF, closePDF
from Adobe_API import renamePDF, deletePages, savePDF, openFile, insertPages
from Adobe_API import getPageCount, zipSinglePDF, extract_delete
from Adobe_API import reversePDF, getPageCount, runPageOCR

def convertAudio(filePath, newType):
    filePath = cleanFilePaths(filePath)
    newType = 'wav'
    b = filePath[:-4] + '.' + newType
    audiotools.open(filePath).convert(b, audiotools.MP3Audio)

def audioSpeed(filePath, speed):
    filePath = cleanFilePaths(filePath)
    cmd = "soundstretch "
    cmd += filePath + ' ' + filePath[:-4] + '2' + filePath[-4:]
    cmd += ' -rate=' + str(speed)
    print cmd
    # system(cmd)

def audioPitch(filePath, pitch):
    filePath = cleanFilePaths(filePath)
    cmd = "soundstretch "
    cmd += filePath + ' ' + filePath[:-4] + '2' + filePath[-4:]
    cmd += ' -pitch=' + str(pitch)
    print cmd
    # system(cmd)

def cleanFilePaths(file_or_files):
    string = True
    if type(file_or_files) == str: 
        string = True
        file_or_files = [file_or_files]
    for i in range(0, len(file_or_files)):
        if filePath.find(' ') != -1: 
            file_or_files[i] = file_or_files[i].replace(' ', '\ ')
        if filePath[len(filePath) - 1] != '/': 
            file_or_files[i] = file_or_files[i] + '/'
    if string == True: return file_or_files[0]
    else: return file_or_files 

if __name__ == '__main__':
    try:
        cmd = []
        cmd.append(os.getcwd() + '/')
        for i in range(1, len(argv)): cmd.append(argv[i])
        # elif cmd[1].find('/') == -1: cmd[1]=os.getcwd()+'/'+cmd[1]
        # print cmd
        stop = False
    except:
        cmd = []
        pass
        # print 'argument error (or testing)'
        # username,password,command='','',''
        stop = True

    if cmd == []: pass
    else:
        print len(cmd)
        
        if cmd[1] == 'convertAudio': convertAudio(cmd[1], cmd[2])
    
        # folderPath='/Users/admin/Desktop/ethics'
        # folderA=os.listdir(folderPath)
        # if folderA.count('.DS_Store') != 0: folderA.pop(folderA.index('.DS_Store'))
        
        # filePath='/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/3_DIV_SCAN/2900_001_OCR_DBL_ODD_0.pdf'
        # print checkFilePathExists(filePath)
        '''
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
        '''

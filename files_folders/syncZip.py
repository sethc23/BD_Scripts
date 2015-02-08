import os
from appscript import *


def getFilesInfo(files):
    fileNames, fileTypes, filePaths = [], [], []
    for item in files:
        item = str(item)
        if item[item.rfind('.') + 1:item.rfind("[")] == 'folders':
            fileTypes.append('folder')
            fileNames.append(item[item.rfind('[') + 3:item.rfind(']') - 2])
            path = '/'
            for part in item.split('folders[u'):
                if part[0] == "'":
                    path = path + part[1:part[2:].find("'") + 2] + '/'
            filePaths.append(path[:-1])
        else:
            fileTypes.append(item[item.rfind('.') + 1:item.rfind("'")])
            fileNames.append(item[item.rfind('[') + 3:item.rfind('[') + item[item.rfind('['):].rfind('.')])
        
            path = '/'
            for part in item.split('folders[u'):
                if part[0] == "'":
                    path = path + part[1:part[2:].find("'") + 2] + '/'
            filePaths.append(path)
    return fileNames, fileTypes, filePaths

def getAllFolderItems(root):
    syncItems = []
    nextFolders = []
    for item in os.listdir(root):
        if os.path.isdir(root + '/' + item) == True:
            nextFolders.append(root + '/' + item)
        else:
            if item.find('.') != 0:
                syncItems.append(root + '/' + item)
    # print '--',nextFolders
    while len(nextFolders) != 0:
        for pt in nextFolders:
            # print 'start folder ',pt
            # print ''
            for subitem in os.listdir(pt):
                # print 'sub-pt ',pt+'/'+subitem
                if subitem.find('.') == 0:
                    pass
                elif os.path.isdir(pt + '/' + subitem) == True:
                    # print 'add folder ',pt+'/'+subitem
                    nextFolders.append(pt + '/' + subitem)
                else:
                    # print pt
                    if subitem.find('.') != 0:
                        syncItems.append(pt + '/' + subitem)
            # print 'remove folder ',nextFolders[nextFolders.index(pt)]
            z = nextFolders.pop(nextFolders.index(pt))
    return syncItems

def prepZip(selectFolder):
    volumes = os.listdir('/Volumes')
    for item in volumes:
        if item.lower().find('lexar') != -1:
            startVol = '/Volumes/' + item
            zipFolder = ''
            for pts in os.listdir(startVol):
                if pts.lower().find(selectFolder) != -1:
                    zipFolder = startVol + '/' + pts
            if zipFolder == '':
                zipFolder = startVol + '/' + selectFolder
                os.makedirs(zipFolder)
            else:
                break
    return startVol

def copyToZip(selectFolder):
    volumes = os.listdir('/Volumes')
    for item in volumes:
        if item.lower().find('lexar') != -1:
            startVol = '/Volumes/' + item
            zipFolder = ''
            for pts in os.listdir(startVol):
                if pts.lower().find(selectFolder) != -1:
                    zipFolder = startVol + '/' + pts
            if zipFolder == '':
                zipFolder = startVol + '/' + selectFolder
                os.makedirs(zipFolder)
            else:
                break
    return startVol

def clean_shell_path(item):
    if item.find(' ') != -1:
        x = item.split(' ')
        z = x[0]
        for i in range(1, len(x)):
            if i != len(x):
                z = z + '\\ ' + x[i]
            else:
                z = z + x[i]
        item = z
    return item

#------------------------------------------------------------------------
#------------------------------------------------------------------------

try:
    for arg in sys.argv:
        printPerPage = arg
except:
    pass

app(u'Finder').activate()
selectedFiles = app(u'Finder').selection.get()
fileNames, fileTypes, filePaths = getFilesInfo(selectedFiles)

##----
root = filePaths[0]
# #---- change to iterable variable
syncItems = getAllFolderItems(root)

selectFolder = root[root[:-1].rfind('/'):].replace('/', '')
zipFolder = prepZip(selectFolder)

zipItems = []
for item in syncItems:
    zipItems.append(zipFolder + '/' + item[item.find(selectFolder):])

'''
for item in syncItems:
    print item
print '---'
for item in zipItems:
    print item
'''
# '''
for i in range(0, len(zipItems)):
    item = zipItems[i]
    x = 'cp ' + clean_shell_path(syncItems[i]) + ' ' + clean_shell_path(zipItems[i])
    # print x
    if os.path.exists(item[:item.rfind('/')]):
        # print 'copy ',item
        os.system(x)
    else:
        checkZip = item[:item.rfind('/')]
        rootZip = checkZip[:checkZip.find(selectFolder) + len(selectFolder) + 1]
        newZip = checkZip[len(rootZip):]
        foldersFromRoot = checkZip[checkZip.find(selectFolder) + len(selectFolder) + 1:].count('/')
        pt = 0
        for i in range(0, foldersFromRoot + 1):
            if i != foldersFromRoot:
                newFolder = rootZip + newZip[:newZip.find('/', pt)]
                pt = len(newZip[:newZip.find('/', pt)]) + 1
            else:
                newFolder = rootZip + newZip
            if os.path.exists(newFolder):
                pass
            else:
                os.makedirs(newFolder)
                # print 'make ',newFolder
        # print 'copy ',item
        os.system(x)
    # print ''
# '''

# ##need to include modified date check

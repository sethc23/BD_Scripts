import os


os.chdir('/Users/admin/Movies/DivX Movies/Temporary Downloaded Files')
workDir = os.getcwd()

files = os.listdir(str(workDir))


allAVIs = []
fileSizes = []
newNames = []
for item in files:
    if item.find('.avi') != -1 and item.find('.part') != -1:
        allAVIs.append(item)
        fileSizes.append(str(os.stat(str(workDir) + '/' + item).st_size))
        newNames.append(item[:item.find('.avi') + 4])

noDupeList = []
for item in newNames:
    if noDupeList.count(item) == 0:
        noDupeList.append(item)


for item in noDupeList:
    renameList = []
    deleteList = []
    indexList = []
    for i in range(0, len(allAVIs)):
        if item == allAVIs[i][:allAVIs[i].find('.avi') + 4]:
            indexList.append(i)
    size = 0
    renamePt = 0
    for num in indexList:
        if fileSizes[num] > size:
            size = fileSizes[num]
            renamePt = indexList.index(num)
        deleteList.append(allAVIs[num])
    renameList.append(deleteList.pop(renamePt))
                         
    for item in deleteList:
        os.remove(workDir + '/' + item)
        # print 'del= ',workDir+'/'+item

    for item in renameList:
        old = workDir + '/' + item
        new = workDir + '/' + item[:item.find('.avi') + 4]
        os.rename(old, new)
        # print 'old= ',old
        # print 'new= ',new

    # print ''
    # print ''

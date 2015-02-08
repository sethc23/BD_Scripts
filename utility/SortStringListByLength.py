

def SortStringListByLength(stringList):
    lenIndex = []
    for j in range(0, len(stringList)):
        lenIndex.append(len(stringList[j]))
    charCount = []
    repCount = 0
    indCount = 0
    totalListLen = len(stringList)
    while totalListLen != 0:
        charCount.append(lenIndex[indCount])
        repCount = lenIndex[indCount:].count(lenIndex[indCount])
        indCount = indCount + repCount
        totalListLen = totalListLen - repCount
    charCount.sort()
    lenIndexCopy = lenIndex[:]
    lenIndexCopy.reverse()
    newList = []
    for i in range(0, len(charCount)):
        start = lenIndex.index(charCount[i])
        end = len(lenIndex) - lenIndexCopy.index(charCount[i])
        newList.extend(stringList[start:end])
    return newList



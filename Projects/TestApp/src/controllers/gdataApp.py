from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
import os
from time import strftime, localtime, time
import datetime
import getData, queryData, debug, sortData, htmlData, DBclasses
from DBclasses import *
import gdata_spreadsheet
import gdata
_DEBUG = True
from postCount import getLocationSubCate

def ManageDataApp(self, action):
    requestType = action
    if requestType == 'gdata prep':
        verifyGdata = PrepApp(self)
        if verifyGdata == 'bounceback':
            return "run again"
        elif verifyGdata.find('complete') == 0:
            return "redirect-/?gdata_result=" + verifyGdata[9:]
        elif verifyGdata.find('error') == 0:
            return verifyGdata
    elif requestType == 'gdata copy':
        copyToGdata = CopyApp(self)
        if copyToGdata == 'bounceback':
            return "run again"
        elif copyToGdata.find('complete') == 0:
            return "redirect-/?gdata_result=" + copyToGdata[9:]
        elif copyToGdata.find('error') == 0:
            return copyToGdata
    elif requestType == 'run gdata':
        runGdata = runGdataApp(self)
        if runGdata == 'bounceback':
            return "run again"
        elif runGdata.find('redirect') == 0:
            return runGdata
        elif runGdata.find('complete') == 0:
            return "redirect-/?gdata_result=" + runGdataApp[9:]
        elif runGdata.find('error') == 0:
            return copyToGdata
    else:
        return "error: unknown argument to ManageDataApp in gdataApp.py"

def PrepApp(self):
    dbStatusCheck = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE runStatus = 'active'")
    dbResults = dbStatusCheck.get()
    if dbResults != None:
        variables = ['workbook', 'stepNum', 'categories', 'cateNum', 'cities', 'cityNum']
        variables.extend(['worksheet', 'WKSHstatus', 'dateHeaders', 'batchStr'])
        propList, valueList = [], []
        for prop in dbResults.properties():
            propList.append(prop)
            valueList.append(dbResults.__getattribute__(prop))
        listVars = ['categories', 'cities', 'dateHeaders']
        for i in range(0, len(propList)):
            if variables.count(str(propList[i])) != 0:
                if str(propList[i]) == 'batchStr':
                    batchStr = str(valueList[i])
                elif listVars.count(str(propList[i])) != 0 and valueList[i] != None:
                    exec "%s=%s" % (propList[i], str(valueList[i]))
                else:
                    exec '%s="%s"' % (propList[i], valueList[i])
    else:
        dbStatusCheck = db.GqlQuery("SELECT * FROM RunTimeVariable " + 
             "WHERE appVariable = 'runGdataApp' " + 
             "AND A_str = 'copyApp'")
        dbResults = dbStatusCheck.get()
        if dbResults != None:
            entryDate = dbResults.B_str
        else:
            entryDate = queryData.getOldestDate() 
            if entryDate == "failure":
                return str('error - gdataApp - getting oldest date for workbook title')
        runStatus, workbook, stepNum = 'active', str(entryDate), 1
        variables = runStatus, workbook, stepNum
        sendData = queryData.startGdataWB(variables)
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 1:
        check = gdata_spreadsheet.main(self, 'makeWorkbook', workbook)
        if check == 'run same again' or check == None:
            stepNum = 2
            variables = stepNum
            varIndex = [2]
            sendData = queryData.updateGdataWB(variables, varIndex, 'active')
            return 'bounceback'
        else:
            return str('error - ' + str(check))
    if int(stepNum) == 2:
        url = "http://geo.craigslist.org/iso/us"
        cities, cityUrls = getData.getSiteUrls(url)
        top_category = "for sale"
        categories, cateUrls = getLocationSubCate(cityUrls[0], top_category)
        categories, cateNum, cities, cityNum = categories, len(categories) - 1, cities[:], len(cities)
        stepNum, worksheet, WKSHstatus = 3, categories[0], 'nextWS'
        variables = stepNum, categories, cateNum, cities, cityNum, worksheet, WKSHstatus
        varIndex = [2, 3, 4, 5, 6, 7, 8]
        sendData = queryData.updateGdataWB(variables, varIndex, 'active')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 3:
        z = str(workbook) + ' Day 1'
        print z
        x = datetime.datetime.strptime(z, "CLcount %Y - Week %W Day %w")
        d = datetime.timedelta(days=1)
        dateHeaders = []
        dateHeaders.append('Cities')
        for i in range(0, 7):
            day = x + (i * d)
            z = str(day.month) + '/' + str(day.day) + '/' + str(day.year)
            dateHeaders.append(z)
        stepNum = 4
        variables = stepNum, dateHeaders
        varIndex = [2, 9]
        sendData = queryData.updateGdataWB(variables, varIndex, 'active')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 4:
        if WKSHstatus == 'nextWS':
            allSheets = gdata_spreadsheet.main(self, 'getWorksheets', workbook)
            if allSheets == 'run same again':
                return 'bounceback'
            if len(allSheets) != 1:
                for i in range(0, len(allSheets)):
                    if categories.count(allSheets[i]) != 0:
                        pt = categories.index(allSheets[i])
                        categories.pop(pt)
            if len(categories) != 0:
                WSlist, row_count, col_count = categories[0], int(cityNum) + 1, len(dateHeaders)
                worksheet = WSlist, row_count, col_count
                variables = workbook, worksheet
                check = gdata_spreadsheet.main(self, 'makeWorksheet', variables)
                if check == 'run same again':
                    return 'bounceback'
                stepNum, worksheet = 5, categories[0]
                variables = stepNum, worksheet
                varIndex = [2, 7]
                sendData = queryData.updateGdataWB(variables, varIndex, 'active')
                if str(sendData) == 'success':
                    return 'bounceback'
                else:
                    return str('error - ' + str(sendData))
            else:
                runStatus = 'complete'
                variables = runStatus
                varIndex = [0]
                sendData = queryData.updateGdataWB(variables, varIndex, 'active')
                if str(sendData) == 'success':
                    return 'redirect-/gdata?action=run+gdata'
                else:
                    return str('error - ' + str(sendData))
    if int(stepNum) == 5:
        cellRefs, cellValues = [], []
        variables = workbook, worksheet, 1
        firstRow = gdata_spreadsheet.main(self, 'getRow', variables)
        if firstRow == 'run same again':
            return 'bounceback'
        if len(firstRow) != len(dateHeaders):
            for i in range(1, len(dateHeaders) + 1):  # +1 for 'cities', +1 for starting w/ 1
                cellRefs.append('R1C' + str(i))
                cellValues.append(dateHeaders[i - 1])
        # Get column...#workbook,worksheet,cities, (cellRefs,cellValues = [],[])
        variables = workbook, worksheet, 'A'
        firstCol = gdata_spreadsheet.main(self, 'getCol', variables)
        if firstCol == 'run same again':
            return 'bounceback'
        if len(firstCol[1]) == 0: 
            for j in range(1, len(cities) + 1):
                row = j + 1
                cellRefs.append('R' + str(row) + 'C1')
            cellValues.extend(cities[:])
        if len(cellRefs) != len(cellValues):
            return "error: - unequal cell/values when making batch"
        elif len(cellRefs) == 0:
            WKSHstatus = 'nextWS'
            stepNum = 4
            variables = stepNum, WKSHstatus
            varIndex = [2, 8]
            sendData = queryData.updateGdataWB(variables, varIndex, 'active')
            if str(sendData) == 'success':
                return 'bounceback'
            else:
                return str('error - ' + str(sendData))
        elif len(cellRefs) == len(cellValues):
            batchStr = cellRefs, cellValues
            stepNum = 6
            variables = stepNum, batchStr
            varIndex = [2, 10]
            sendData = queryData.updateGdataWB(variables, varIndex, 'active')
            if str(sendData) == 'success':
                return 'bounceback'
            else:
                return str('error - ' + str(sendData))
        else:
            return "unknown error in step 5 of prep app"
    if int(stepNum) == 6:
        listNum = len(eval(batchStr))
        if listNum == 2:
            cellRefs, cellValues = eval(batchStr)
            cellVerKeys = []
        elif listNum == 3:
            cellRefs, cellValues, cellVerKeys = eval(batchStr)
        variables = workbook, worksheet, cellRefs, cellValues, cellVerKeys, batchStr, 'active'
        sendData = makeBatch(self, variables)
        # batchStr,cellRefs,cellValues
        if str(sendData) == 'success' or str(sendData) == 'bounceback':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 7:
        cellRefs, cellValues, cellVerKeys = eval(batchStr)
        if len(cellRefs) != len(cellVerKeys):
            return 'error: step7 in prepApp - uneven cellRefs to cellVerKeys'
        variables = workbook, worksheet, cellRefs, cellValues, cellVerKeys, None
        # next arg recognizes no batchStr and returns one
        batchStr = gdata_spreadsheet.main(self, 'makebatchStr', variables)
        if batchStr == 'run same again':
            return 'bounceback'
        stepNum = 8
        variables = stepNum, batchStr
        varIndex = [2, 10]
        sendData = queryData.updateGdataWB(variables, varIndex, 'active')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 8:
        variables = workbook, worksheet, None, None, batchStr
        check = gdata_spreadsheet.main(self, 'addWKSHvalues', variables)
        if check == 'run same again':
            return 'bounceback'
        stepNum, WKSHstatus, batchStr = 4, 'nextWS', ''
        variables = stepNum, WKSHstatus, batchStr
        varIndex = [2, 8, 10]
        sendData = queryData.updateGdataWB(variables, varIndex, 'active')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
#        runStatus,workbook, stepNum,categories,cateNum,
#            0    ,    1   ,   2    ,    3     ,   4    
#        cities, cityNum, worksheet,  WKSHstatus, dateHeaders, postStr
#            5 ,    6   ,     7    ,    8     ,     9            10



def CopyApp(self):
    dbStatusCheck = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE runStatus = 'copying'")
    dbResults = dbStatusCheck.get()
    if dbResults != None:
        variables = ['workbook', 'stepNum', 'categories', 'cateNum', 'cities', 'cityNum']
        variables.extend(['worksheet', 'WKSHstatus', 'dateHeaders', 'batchStr'])
        propList, valueList = [], []
        for prop in dbResults.properties():
            propList.append(prop)
            valueList.append(dbResults.__getattribute__(prop))
        listVars = ['categories', 'cities', 'dateHeaders']
        for i in range(0, len(propList)):
            if variables.count(str(propList[i])) != 0:
                if str(propList[i]) == 'batchStr':
                    batchStr = str(valueList[i])
                elif listVars.count(str(propList[i])) != 0 and valueList[i] != None:
                    exec "%s=%s" % (propList[i], str(valueList[i]))
                else:
                    exec '%s="%s"' % (propList[i], valueList[i])
    else:
        dbStatusCheck = db.GqlQuery("SELECT * FROM RunTimeVariable " + 
             "WHERE appVariable = 'runGdataApp' " + 
             "AND A_str = 'copyApp'")
        dbResults = dbStatusCheck.get()
        if dbResults != None:
            entryWeek = dbResults.B_str
            dbStatusCheck = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE workbook = :1", str(entryWeek))
            dbResults = dbStatusCheck.get()
            if dbResults != 0:
                runStatusDB = dbResults.runStatus
            runStatus, stepNum = 'copying', 2
            variables = runStatus, stepNum
            varIndex = [0, 2]
            sendData = queryData.updateGdataWB(variables, varIndex, str(runStatusDB))
            if str(sendData) == 'success':
                return 'bounceback'
            else:
                return str('error - ' + str(sendData))
        else:
            entryDate = queryData.getOldestDate() 
            x = str(entryDate)
            xl = len(x)
            year, date, month = x[xl - 2:], x[xl - 4:xl - 2], x[0:xl - 4]
            dateStr = str(year) + ' - ' + str(date) + ' - ' + str(month)
            entryDate = datetime.datetime.strptime(dateStr, '%y - %d - %m') 
            entryWeek = entryDate.strftime("CLcount %Y - Week %W")
            check = gdata_spreadsheet.main(self, 'makeWorkbook', str(entryWeek))
            if check == 'run same again':
                return 'bounceback'
            runStatus, workbook, stepNum, = 'copying', entryWeek, 2
            variables = runStatus, workbook, stepNum
            sendData = queryData.startGdataWB(variables)
            if str(sendData) == 'success':
                return 'bounceback'
            else:
                return str('error - ' + str(sendData))

    if int(stepNum) == 2:
        entryDate = queryData.getOldestDate() 
        x = str(entryDate)
        xl = len(x)
        year, date, month = x[xl - 2:], x[xl - 4:xl - 2], x[0:xl - 4]
        if date[0] == '0':
            date = date[1]
        dateStr = str(month) + '/' + str(date) + '/20' + str(year)
        if len(dateStr) == 7:
            dateStr = '0' + dateStr
        colIndex = dateHeaders.index(dateStr) - 1
        alphabet = 'ABCDEFHIJKLMNOPQRSTUVWXYZ'
        colLetter = alphabet[(colIndex + 1)]
        worksheet = categories[eval(cateNum) - 1]
        cateNum = eval(cateNum) - 1
        variables = workbook, worksheet, colLetter
        existCol = gdata_spreadsheet.main(self, 'getCol', variables)
        if existCol == 'run same again':
            return 'bounceback'
        if len(existCol[1]) != 0:
            # get all cities with date and category from PostCount
            countData, lastDate = queryData.getCategoryCount(entryDate, worksheet, None)
            cityRefs, postCounts = [], []
            for entry in countData:
                cityRefs.append(str(entry.city))
                postCounts.append(str(entry.postCount))
            attempts = 4
            while lastDate != '' and attempts != 0:
                moreData, lastDate = queryData.getCategoryCount(entryDate, worksheet, lastDate)
                for entry in moreData:
                    cityRefs.append(str(entry.city))
                    postCounts.append(str(entry.postCount))
                # countData.extend(moreData)
                attempts = attempts - 1
        entryCount = queryData.getCategoryEntryCount(entryDate, worksheet, None)
        if lastDate == '' and len(postCounts) == entryCount[0]:
            colIndex = dateHeaders.index(dateStr)
            colIndex = colIndex + 1
            cellValues, cellRefs = [], []
            for i in range(0, len(postCounts)):
                cellValues.append(postCounts[i])
                rowNum = cities.index(cityRefs[i]) + 2
                cellRefs.append('R' + str(rowNum) + 'C' + str(colIndex))
        else:
            print 'different postCounts and entryCounts'
            print 'worksheet: ', worksheet
            print 'entryCount: ', entryCount[0]
            print 'postCounts: ', postCounts
            # return 'bounceback'
        if len(postCounts) == len(cellValues):
            batchStr = cellRefs, cellValues
            stepNum = 3
            variables = stepNum, cateNum, worksheet, batchStr
            varIndex = [2, 4, 7, 10]
            sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
            if str(sendData) == 'success':
                return 'bounceback'
            else:
                return str('error - ' + str(sendData))
    if int(stepNum) == 3:
        listNum = len(eval(batchStr))
        if listNum == 2:
            cellRefs, cellValues = eval(batchStr)
            cellVerKeys = []
        elif listNum == 3:
            cellRefs, cellValues, cellVerKeys = eval(batchStr)
        variables = workbook, worksheet, cellRefs, cellValues, cellVerKeys, batchStr, 'copying'
        sendData = makeBatch(self, variables)
        if sendData == 'bounceback' or str(sendData) == 'bounceback':
            return 'bounceback'
        elif str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 4:
        cellRefs, cellValues, cellVerKeys = eval(batchStr)
        if len(cellRefs) != len(cellVerKeys):
            return 'error: step4 in copyApp - uneven cellRefs to cellVerKeys'
        variables = workbook, worksheet, cellRefs, cellValues, cellVerKeys, None
        # next arg recognizes no batchStr and returns one
        batchStr = gdata_spreadsheet.main(self, 'makebatchStr', variables)
        if batchStr == 'run same again':
            return 'bounceback'
        stepNum = 5
        variables = stepNum, batchStr
        varIndex = [2, 10]
        sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 5:
        variables = workbook, worksheet, None, None, batchStr
        check = gdata_spreadsheet.main(self, 'addWKSHvalues', variables)
        if check == 'run same again':
            return 'bounceback'
        if str(cateNum) == '0':
            cateNum = len(categories)
            stepNum = 6
        else:
            stepNum = 2
        batchStr = ''
        variables = stepNum, cateNum, batchStr
        varIndex = [2, 4, 10]
        sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
    if int(stepNum) == 6:
        # #Get count of entries that should have been added
        entryDate = queryData.getOldestDate()
        cityRefs, postCounts = [], []
        countData, lastDate = queryData.getEntryDateCount(entryDate, None)
        attempts = 7
        while lastDate != '' and attempts != 0:
            moreData, lastDate = queryData.getEntryDateCount(entryDate, lastDate)
            countData = countData + moreData
            attempts = attempts - 1
        stepNum, worksheet, batchStr = 7, categories[len(categories) - 1], [countData]
        variables = stepNum, worksheet, batchStr
        varIndex = [2, 7, 10]
        sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
        if str(sendData) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(sendData))
#        runStatus,workbook, stepNum,categories,cateNum,
#            0    ,    1   ,   2    ,    3     ,   4    
#        cities, cityNum, worksheet,  WKSHstatus, dateHeaders, postStr
#            5 ,    6   ,     7    ,    8     ,     9            10
    if int(stepNum) == 7:
        entryDate = queryData.getOldestDate()
        variables = workbook, categories, cateNum, worksheet, dateHeaders, batchStr, entryDate
        check = countGdataColumnData(self, variables)
        if str(check) == 'success':
            return 'bounceback'
        else:
            return str('error - ' + str(check)) 
    if int(stepNum) == 8:
        entryDate = queryData.getOldestDate()
        x = str(entryDate)
        xl = len(x)
        year, date, month = x[xl - 2:], x[xl - 4:xl - 2], x[0:xl - 4]
        if date[0] == '0':
            date = date[1]
        dateStr = str(month) + '/' + str(date) + '/20' + str(year)
        if len(dateStr) == 7:
            dateStr = '0' + dateStr
        colIndex = dateHeaders.index(dateStr) - 1
        alphabet = 'ABCDEFHIJKLMNOPQRSTUVWXYZ'
        colLetter = alphabet[(colIndex + 1)]
        DBEntryCount, gDataColumns = eval(batchStr)
        gdateEntryCount = len(gDataColumns) - gDataColumns.count(str(colLetter) + '1')
        if DBEntryCount[0] == gdateEntryCount:
            variables = 'postDate', '=', entryDate
            result = queryData.deleteEntryByVariable('PostCount', variables, '40')
            if str(result) == "data deleted":
                return "run again"
            else:
                runStatus = 'complete'
                stepNum, cateNum, batchStr = 2, len(categories), ''
                variables = runStatus, stepNum, worksheet, batchStr
                varIndex = [0, 2, 7, 10]
                sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
                if str(sendData) == 'success':
                    queryData.deleteRuntimeVar('runGdataApp')
                    return 'redirect-/gdata?action=run+gdata'
                else:
                    return str('error - ' + str(sendData))
        else:
            return 'error - in CopyApp, DB count != gData count'

def runGdataApp(self):
    firstCheck = queryData.getRunTimeVariable('runGdataApp')
    if str(firstCheck) != 'No DB entry to return':
        target = firstCheck.A_str
        if target == 'prepApp':
            dbStatusCheck = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE runStatus = 'complete'")
            dbResults = dbStatusCheck.get()
            if dbResults != None:
                appVariable, A_str, B_str = 'runGdataApp', 'copyApp', str(dbResults.workbook)
                variables = A_str, B_str
                varIndex = [3, 4]
                queryData.updateRuntimeVariable(A_str, varIndex, appVariable)
                return 'redirect-/gdata?action=gdata+copy'
            else:
                return 'redirect-/gdata?action=gdata+prep'
        elif target == 'copyApp':
            return 'redirect-/gdata?action=gdata+copy'
        else:
            return 'error: runGdataApp, unknown target'
    else:    
        nextOldestDate = queryData.getOldestDate()
        if nextOldestDate != 'failure':
            x = str(nextOldestDate)
            xl = len(x)
            year, date, month = x[xl - 2:], x[xl - 4:xl - 2], x[0:xl - 4]
            dateStr = str(year) + ' - ' + str(date) + ' - ' + str(month)
            entryDate = datetime.datetime.strptime(dateStr, '%y - %d - %m') 
            entryWeek = entryDate.strftime("CLcount %Y - Week %W")
            check = gdata_spreadsheet.main(self, 'checkForWorkbook', str(entryWeek))
            if check == 'run same again' or check == 'error on server':
                return 'bounceback'
            dbStatusCheck = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE workbook = :1", str(entryWeek))
            dbResults = dbStatusCheck.get()
            if dbResults != None:
                runStatus = dbResults.runStatus
            if runStatus == 'active' or check == 'failure':
                appVariable, A_str, B_str = 'runGdataApp', 'prepApp', str(entryWeek)
                variables = appVariable, A_str, B_str
                varIndex = [0, 3, 4]
                queryData.updateRuntimeVariable(variables, varIndex, None)
                return 'redirect-/gdata?action=gdata+prep'
            elif (check == 'success' and runStatus == 'complete') or runStatus == 'copying':
                appVariable, A_str, B_str = 'runGdataApp', 'copyApp', str(entryWeek)
                variables = appVariable, A_str, B_str
                varIndex = [0, 3, 4]
                queryData.updateRuntimeVariable(variables, varIndex, None)
                return 'redirect-/gdata?action=gdata+copy'
            elif runStatus == 'copied':
                appVariable, A_str, B_str = 'runGdataApp', 'copyApp', str(entryWeek)
                variables = appVariable, A_str, B_str
                varIndex = [0, 3, 4]
                queryData.updateRuntimeVariable(variables, varIndex, None)
                runStatus, stepNum, worksheet = 'copying', 2, str(entryWeek)
                variables = runStatus, stepNum, worksheet
                varIndex = [0, 2, 7]
                sendData = queryData.updateGdataWB(variables, varIndex, 'copied')
                return 'redirect-/gdata?action=gdata+copy'
        else:
            return "redirect-/?gdata_result=all gdata updated"

    
#        appVariable, A_int, B_int  , A_str   , B_str , C_str
#            0    ,    1   ,   2    ,    3    ,   4   ,  5
#        D_str , E_str , A_bool , B_bool , A_date 
#            6 ,    7  ,   8    ,   9    ,    10           


def makeBatch(self, variables):
    workbook, worksheet, cellRefs, cellValues, cellVerKeys, batchStr, runStatus = variables
    requestSize = 10
    iterNum = (len(cellRefs) - len(cellVerKeys)) / requestSize
    extra = (len(cellRefs) - len(cellVerKeys)) - (requestSize * iterNum)
    finished = False
    if iterNum == 0 and extra != 0:
        iterNum = 0
    elif iterNum == 0 and extra == 0:
        finished = True
    now = int(time())
    end = now + (17)
    attempts = 10
    while end >= now and attempts != 0 and finished == False:
        for i in range(0, iterNum + 1):
            sIndex = len(cellVerKeys)
            if i == iterNum and extra != 0:
                eIndex = sIndex + extra
            elif i == iterNum and extra == 0:
                finished = True
                break
            else:
                eIndex = sIndex + requestSize
            variables = workbook, worksheet, cellRefs[sIndex:eIndex], cellValues[sIndex:eIndex]
            newCellVerKeys = gdata_spreadsheet.main(self, 'getCellVersions', variables)
            if newCellVerKeys == 'run same again':
                return 'bounceback'
            if type(newCellVerKeys) != list:
                finished = False
                break
            else:
                cellVerKeys.extend(newCellVerKeys)
            now = int(time())
            attempts = attempts - 1
            if now > end or attempts == 0:
                finished = False
                break
            if i == iterNum:
                finished = True
                break
    if runStatus == 'active':
        if finished == True:
            stepNum = 7
        elif finished == False:
            stepNum = 6
    elif runStatus == 'copying':
        if finished == True:
            stepNum = 4
        elif finished == False:
            stepNum = 3
    batchStr = cellRefs, cellValues, cellVerKeys 
    variables = stepNum, batchStr
    varIndex = [2, 10]
    sendData = queryData.updateGdataWB(variables, varIndex, runStatus)
    return sendData

def countGdataColumnData(self, variables):
    workbook, categories, cateNum, worksheet, dateHeaders, batchStr, entryDate = variables
    if len(eval(batchStr)) == 1:
        gDataCount = eval(batchStr)
        gDataColumns = []
    elif len(eval(batchStr)) == 2:
        gDataCount, gDataColumns = eval(batchStr)
    x = str(entryDate)
    xl = len(x)
    year, date, month = x[xl - 2:], x[xl - 4:xl - 2], x[0:xl - 4]
    if date[0] == '0':
        date = date[1]
    dateStr = str(month) + '/' + str(date) + '/20' + str(year)
    if len(dateStr) == 7:
        dateStr = '0' + dateStr
    colIndex = dateHeaders.index(dateStr) - 1
    alphabet = 'ABCDEFHIJKLMNOPQRSTUVWXYZ'
    colLetter = alphabet[(colIndex + 1)]
    now = int(time())
    end = now + (17)
    attempts = 35
    if str(cateNum) == '0':
        finished = True
    else:
        finished = False
#    if totalL == 0:
#        worksheet = categories[0]
#        variables = workbook,worksheet,colLetter
#        existCol = gdata_spreadsheet.main(self,'getCol',variables)
#        if existCol == 'run same again':
#            return 'bounceback'
#        elif type(existCol) != tuple:
#            finished = False
#        else:
#            gDataColumns.extend(existCol[0])
#            finished = True
    #########
    while end >= now and attempts != 0 and finished == False:
        for i in range(0, eval(cateNum)):
            variables = workbook, worksheet, colLetter
            existCol = gdata_spreadsheet.main(self, 'getCol', variables)
            if existCol == 'run same again':
                return 'bounceback'
            if type(existCol) != tuple:
                finished = False
                break
            else:
                gDataColumns.extend(existCol[0])
                cateNum = str(eval(cateNum) - 1)
                worksheet = categories[eval(cateNum) - 1]
            now = int(time())
            attempts = attempts - 1
            if now > end or attempts == 0:
                finished = False
                break
            if str(cateNum) == '0':
                finished = True
                break
        break
    #########
    if finished == True:
        stepNum = 8
    elif finished == False:
        stepNum = 7
    batchStr = gDataCount, gDataColumns
    variables = stepNum, cateNum, worksheet, batchStr
    varIndex = [2, 4, 7, 10]
    sendData = queryData.updateGdataWB(variables, varIndex, 'copying')
    return sendData

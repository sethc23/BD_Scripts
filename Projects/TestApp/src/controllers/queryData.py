from google.appengine.ext import db
from controllers.DBclasses import *
from datetime import datetime
_DEBUG = True

def getOneCity():
    oneCityQuery = Locations.gql("WHERE updated = False")
    x = oneCityQuery.get()
    if x != None:
        return x
    else:
        return "Nothing to Update"

def getOldestDate():
    oneDateQuery = PostCount.gql("ORDER BY postDate")
    x = oneDateQuery.get()
    if x != None:
        return x.postDate
    else:
        return "failure"

def getNewCategory():
    oneCateQuery = Hierarchy.gql("WHERE counted = False ORDER BY random")
    try:
        x = oneCateQuery.get()
        status = x.counted
        return x
    except:
        return "Nothing to Update"

def getOneCategory(url):
    CateQuery = Hierarchy.gql("WHERE url = :1", url)
    try:
        x = CateQuery.get()
        return x
    except:
        return "Nothing to Update"

def getDBCount(database, lastDate):
    DBQuery = eval(database).all()
    DBQuery.order("created")
    if DateIndex != None:
        x = str(DateIndex)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        DBQuery.filter("created >", dateFormated)
    x = DBQuery.fetch(100)
    if len(x) == 100:
        lastDate = str(x[99].created)
        return len(x), lastDate
    else:
        return len(x), ""
    
def getCategoryEntryCount(date, category, lastDate):
    DBQuery = PostCount.all()
    DBQuery.filter("postDate =", date)
    DBQuery.filter("category =", category)
    DBQuery.order("created")
    if lastDate != None:
        x = str(lastDate)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        DBQuery.filter("created >", dateFormated)
    x = DBQuery.fetch(100)
    if len(x) == 100:
        lastDate = str(x[99].created)
        return len(x), lastDate
    else:
        return len(x), ""

def getCategoryCount(date, category, lastDate):
    DBQuery = PostCount.all()
    DBQuery.filter("postDate =", date)
    DBQuery.filter("category =", category)
    DBQuery.order("created")
    if lastDate != None:
        x = str(lastDate)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        DBQuery.filter("created >", dateFormated)
    x = DBQuery.fetch(100)
    if len(x) == 100:
        lastDate = str(x[99].created)
        return x, lastDate
    else:
        return x, ""

def getEntryDate(date, lastDate):
    DBQuery = PostCount.all()
    DBQuery.filter("postDate =", date)
    DBQuery.order("created")
    if lastDate != None:
        x = str(lastDate)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        DBQuery.filter("created >", dateFormated)
    x = DBQuery.fetch(100)
    if len(x) == 100:
        lastDate = str(x[99].created)
        return x, lastDate
    else:
        return x, ""

def getEntryDateCount(date, lastDate):
    DBQuery = PostCount.all()
    DBQuery.filter("postDate =", date)
    DBQuery.order("created")
    if lastDate != None:
        x = str(lastDate)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        DBQuery.filter("created >", dateFormated)
    x = DBQuery.fetch(100)
    if len(x) == 100:
        lastDate = str(x[99].created)
        return len(x), lastDate
    else:
        return len(x), ""

def getGdataWBentry(workbook):
    DBquery = gdataDB.gql('WHERE workbook = :1', str(workbook))
    try:
        x = DBquery.get()
        if x == None:
            return "No DB entry to return"
        else:
            return x
    except:
        return "No DB entry to return"

def getRunTimeVariable(appVariable):
    DBquery = RunTimeVariable.gql('WHERE appVariable = :1', str(appVariable))
    try:
        x = DBquery.get()
        if x == None:
            return "No DB entry to return"
        else:
            return x
    except:
        return "No DB entry to return"
  
def checkQueryPosts(postId):
    repeatPosts = []
    if len(postId) == 0:
        return repeatPosts
    else:
        oldpostId = postId[:]
        newpostId = postId[:]
        newpostId.sort()
        small = eval(newpostId[0])
        big = eval(newpostId[len(newpostId) - 1])
        postIdQuery = Categories.gql("WHERE postId >= :1 AND postId <= :2 ORDER BY postId DESC", small, big)
        try:
            x = postIdQuery.get()
        except:
            return repeatPosts
        if postIdQuery.count() == 0:
            return repeatPosts
        postQlist = list(post.postId for post in postIdQuery)
        for i in range(0, len(oldpostId)):
            try:
                a = postQlist.index(long(oldpostId[i]))
                repeatPosts.append(str(postQlist[a]))
            except ValueError:
                pass
        # print len(repeatPosts)
        return repeatPosts

def checkCityUrl(name, url):
    checkCityQuery = Locations.gql("WHERE location = :1 AND url = :2", str(name), str(url))
    try:
        x = checkCityQuery.get()
        status = x.updated
        return str(status)
    except:
        return None

def checkPostCount(city, category, postDate):
    checkPostEntries = PostCount.gql("WHERE city = :1 AND category = :2 AND postDate = :3",
                                     str(city), str(category), int(postDate))
    try:
        x = checkPostEntries.get()
        status = x.postCount
        return 'status:True'
    except:
        return False

def checkCityCateUrl(fullurl):
    checkCityCateQuery = Hierarchy.gql("WHERE url = :1", str(fullurl))
    try:
        x = checkCityCateQuery.get()
        status = x.counted
        return 'status:True'
    except:
        return False

def checkWebPage(url):
    checkWebPage = htmlData.gql("WHERE url = :1", str(url))
    try:
        webpage = checkWebPage.get()
        status = webpage.status
        return webpage
    except:
        return False

def checkVariable(appVariable):
    checkAppVar = RunTimeVariable.gql("WHERE appVariable = :1", str(appVariable))
    try:
        x = checkAppVar.get()
        name = x.appVariable
        return x
    except:
        return False

def updateOneCity(name, url):
    if url == None:
        oneCityQuery = Locations.gql("WHERE updated = False AND location = :1", str(name))
    else:
        oneCityQuery = Locations.gql("WHERE updated = False AND location = :1 " + 
                                 "AND url = :2", str(name), str(url))
    try:
        x = oneCityQuery.get()
        x.updated = True
        x.put()
        return "Updated"
    except:
        return False

def updateOneCategory(location, category):
    oneCateQuery = Hierarchy.gql("WHERE counted = False AND location = :1 " + 
                                 "AND category = :2", str(location), str(category))
    try:
        x = oneCateQuery.get()
        x.counted = True
        x.put()
        return "Updated"
    except:
        return "Error in updating hierarchy status"    
    
def updateWebPage(url, line):
    checkWebPage = htmlData.gql("WHERE url = :1", str(url))
    try:
        webpage = checkWebPage.get()
        webpage.line = int(line)
        webpage.put()
        return "updated"
    except:
        return False

def updateVariable(appVariable, A_int, B_int, A_str, B_str, C_str, D_str, E_str, A_bool, B_bool, A_date):
    checkAppVar = RunTimeVariable.gql("WHERE appVariable = :1", str(appVariable))
    x = checkAppVar.get()
    x.A_int = int(A_int)
    # B_int is error counter
    x.B_int = int(B_int) + x.B_int        
    x.A_str = str(A_str)
    x.B_str = str(B_str)
    x.C_str = str(C_str)
    x.D_str = str(D_str)
    x.E_str = str(E_str)
    x.A_bool = bool(A_bool)
    if x.B_int == 5:
        x.B_bool = False
    else:
        x.B_bool = bool(B_bool)
    if type(A_date) == datetime:
        x.A_date = A_date
    elif A_date == None:
        x.A_date = None
    else:
        y = str(A_date)
        z = datetime.strptime(y[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(y[20:]))
        x.A_date = dateFormated
    try:
        x.put()
        return "Updated"
    except:
        return False

def updateRuntimeVariable(variables, varIndex, appVariable):
    if appVariable != None:
        DBentry = db.GqlQuery("SELECT * FROM RunTimeVariable " + 
                             "WHERE appVariable = :1", str(appVariable))
        dbEntry = DBentry.get()
        if dbEntry == None:
            return "updateGdataWB - no query results to update"
    else:
        dbEntry = RunTimeVariable()
    DBvariables = ['appVariable', 'A_int', 'B_int', 'A_str', 'B_str', 'C_str',
                   'D_str', 'E_str', 'A_bool', 'B_bool', 'A_date']
    line = "Start-"
#        appVariable, A_int, B_int  , A_str   , B_str , C_str
#            0    ,    1   ,   2    ,    3    ,   4   ,  5
#        D_str , E_str , A_bool , B_bool , A_date 
#            6 ,    7  ,   8    ,   9    ,    10           
    if len(varIndex) > 1:
        for i in varIndex:
            # if varIndex.count(i) != 0:  #if varIndex is particular DBvariable and not ""
            if [1, 2].count(i) != 0:  # if this variable is one of the integer property numbers...
                line = line + " int_values: " + str(variables[varIndex.index(i)])
                dbEntry.__setattr__(str(DBvariables[i]), int(variables[varIndex.index(i)]))
            elif [8, 9].count(i) != 0:
                line = line + " bool_values: " + str(variables[varIndex.index(i)])
                dbEntry.__setattr__(str(DBvariables[i]), int(variables[varIndex.index(i)]))
            else:
                line = line + " str_values: " + str(variables[varIndex.index(i)])
                dbEntry.__setattr__(str(DBvariables[i]), str(variables[varIndex.index(i)]))
        dbEntry.put()
    else:
        variable = variables
        if [1, 2].count(varIndex[0]) != 0:  # if this variable is one of the integer property numbers...
            line = line + " int_values: " + str(variable)
            dbEntry.__setattr__(str(DBvariables[varIndex[0]]), eval(str(variable)))
        elif [8, 9].count(varIndex[0]) != 0:
            line = line + " bool_values: " + str(variable)
            dbEntry.__setattr__(str(DBvariables[varIndex[0]]), eval(variable))
        else:
            line = line + " str_values: " + str(variable)
            dbEntry.__setattr__(str(DBvariables[varIndex[0]]), str(variable))
        dbEntry.put()        
    line = "end"
    return "success" 


#        runStatus,workbook, stepNum,categories,cateNum,
#            0    ,    1   ,   2    ,    3     ,   4    
#        cities, cityNum, worksheet,  WKSHstatus, dateHeaders, postStr
#            5 ,    6   ,     7    ,    8     ,     9            10

def updateGdataWB(variables, varIndex, runStatus):
    DBentry = db.GqlQuery("SELECT * FROM gdataDB " + 
                         "WHERE runStatus = :1", str(runStatus))
    dbEntry = DBentry.get()
    if dbEntry == None:
        return "updateGdataWB - no query results to update"
    DBvariables = ['runStatus', 'workbook', 'stepNum', 'categories', 'cateNum', 'cities',
                   'cityNum', 'worksheet', 'WKSHstatus', 'dateHeaders', 'batchStr']
    line = "Start-"
#        runStatus,workbook, stepNum,categories,cateNum,
#            0    ,    1   ,   2    ,    3     ,   4    
#        cities, cityNum, worksheet,  WKSHstatus, dateHeaders, postStr
#            5 ,    6   ,     7    ,    8     ,     9         , 10             
    if len(varIndex) > 1:
        for i in varIndex:
            # if varIndex.count(i) != 0:  #if varIndex is particular DBvariable and not ""
            if [2, 4, 6].count(i) != 0:  # if this variable is one of the integer property numbers...
                line = line + " int_values: " + str(variables[varIndex.index(i)])
                dbEntry.__setattr__(str(DBvariables[i]), int(variables[varIndex.index(i)]))
                dbEntry.put()
            else:
                line = line + " str_values: " + str(variables[varIndex.index(i)])
                dbEntry.__setattr__(str(DBvariables[i]), str(variables[varIndex.index(i)]))
                dbEntry.put()
    else:
        variable = variables
        if [2, 4, 6].count(varIndex[0]) != 0:  # if this variable is one of the integer property numbers...
            line = line + " int_values: " + str(variable)
            dbEntry.__setattr__(str(DBvariables[varIndex[0]]), int(variable))
            dbEntry.put()
        else:
            line = line + " str_values: " + str(variable)
            dbEntry.__setattr__(str(DBvariables[varIndex[0]]), str(variable))
            dbEntry.put()
    line = "end"
    return "success"        
    
def deleteAll(database, packNum):
    querystring = ("SELECT * FROM " + str(database))
    try:
        checkDB = db.GqlQuery(querystring)
    except:
        return "database deleted"
    data = checkDB.fetch(int(packNum))
    num = checkDB.count(int(packNum))
    if num == 0:
        return "database deleted"
    else:
        for result in data:
            result.delete()
        return "data deleted"

def deleteEntryByVariable(database, variables, packNum):
    varName, varSign, varValue = variables
    dbQuery = eval(database).all()
    filterStr = 'WHERE ' + str(varName) + ' ' + str(varSign)
    try:
        dbQuery.filter(filterStr, str(varValue))
    except:
        return "queryDate.deleteEntryByVariable: no entries by filter"
    data = dbQuery.fetch(int(packNum))
    num = dbQuery.count(int(packNum))
    if num == 0:
        return "entries deleted"
    else:
        for result in data:
            result.delete()
        return "data deleted"

def deleteWebPage(url):
    checkWebPage = htmlData.gql("WHERE url = :1", str(url))
    try:
        webpage = checkWebPage.get()
        webpage.delete()
        return "webpage deleted"
    except:
        return False

def deleteRuntimeVar(appVariable):
    checkVariable = RunTimeVariable.gql("WHERE appVariable = :1", str(appVariable))
    try:
        variable = checkVariable.get()
        variable.delete()
        return "variable deleted"
    except:
        return False

def sendData(site, category, titles, links, postId, postDate, postNumber):
    try:
        line = "Start-"
        for i in range(0, postNumber):  # len(titles)):
            line = line + "entry-"
            sub_entry = Categories()
            line = line + " value: " + site
            sub_entry.location = str(site)
            line = line + " value: " + category
            sub_entry.name = str(category)
            line = line + " value: " + titles[i]
            sub_entry.title = str(titles[i])
            line = line + " value: " + links[i]
            sub_entry.link = str(links[i])
            line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
            sub_entry.postId = int(postId[i])
            line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
            sub_entry.postDate = int(postDate[i])
            try:
                line = line + "put-sub"
                sub_entry.put()
            except:
                line = line + "encode-"
                text = titles[i].encode('ASCII', 'elinks')
                line = line + "entry-"
                sub_entry = Categories()
                line = line + " value: " + site
                sub_entry.location = str(site)
                line = line + " value: " + category
                sub_entry.name = str(category)
                line = line + " value: " + titles[i]
                sub_entry.title = str(titles[i])
                line = line + " value: " + links[i]
                sub_entry.link = str(links[i])
                line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
                sub_entry.postId = int(postId[i])
                line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
                sub_entry.postDate = int(postDate[i])
                line = line + "put-sub"
                sub_entry.put()
            line = line + "iteration-"
        line = "end"
        return "success"
    except:
        receivedData = site, category, titles, links, postId, postDate, postNumber
        line = str(receivedData) + "    ----    " + line
        return "sendData failure: " + line

def sendHTML(html, url):
    line = "Start-"
    entry = htmlData()
    line = line + " values: " + "html"
    entry.html = unicode(html)
    line = line + " values: " + url
    entry.url = str(url)
    line = line + " values: " + "line number"   
    entry.line = 0
    line = line + " values: " + "status:false" 
    entry.status = False
    try:
        line = line + "put-sub-"
        entry.put()
    except BadValueError:
        return "bad value: " + line
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendError(error, string1, string2, index, status):
    line = "Start-"
    x = errorData()
    line = line + " values: " + "error"
    x.error = unicode(error)
    line = line + " values: " + str(string1)
    x.string1 = str(string1)
    line = line + " values: " + str(string2)  
    x.string2 = str(string2)
    if index == None:
        line = line + " values: " + str(0) 
        x.index = 0
    else:
        line = line + " values: " + str(index) 
        x.index = int(index)
    if status == True or status == False:
        line = line + " values: " + str(status) 
        x.status = status
    else:    
        line = line + " values: " + "status:false" 
        x.status = False
    created = db.DateTimeProperty(auto_now_add=True)
    try:
        line = line + "put-sub-"
        x.put()
    except BadValueError:
        return "bad value: " + line
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendPostCount(location, category, postDate, postCount):
    line = "Start-"
    line = line + "entry-"
    sub_entry = PostCount()
    line = line + " value: " + location
    sub_entry.city = str(location)
    line = line + " value: " + category
    sub_entry.category = str(category)
    line = line + " values: " + str(postDate)
    sub_entry.postDate = int(postDate)
    line = line + " values: " + str(postCount)
    sub_entry.postCount = int(postCount)
    try:
        line = line + "put-sub"
        sub_entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendCountSchedule(url):
    line = "Start-"
    for i in range(0, len(url)):
        line = line + "entry-"
        entry = Hierarchy()
        line = line + " values: " + str(url[i])
        entry.url = str(url[i])
        try:
            line = line + "put-sub"
            entry.put()
        except:
            return "sendData failure: " + line 
        line = line + "iteration-"
    line = "end"
    return "success"

def sendOneCity(location, url):
    line = "Start-"
    entry = Locations()
    line = line + " values: " + location
    entry.location = str(location)        
    line = line + " values: " + url
    entry.url = str(url)
    entry.updated = False  # updated meaning is category checked
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendCityCate(location, category, fullurl, random):
    line = "Start-"
    entry = Hierarchy()
    line = line + " values: " + location
    entry.location = str(location)
    line = line + " values: " + category
    entry.category = str(category)        
    line = line + " values: " + fullurl
    entry.url = str(fullurl)
    entry.random = int(random)
    entry.counted = False
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def sendVariable(appVariable, A_int, B_int, A_str, B_str, C_str, D_str, E_str, A_bool, B_bool, A_date):
    line = "Start-"
    entry = RunTimeVariable()
    line = line + " values: " + str(appVariable)
    entry.appVariable = str(appVariable)
    if A_int == None:
        A_int = 0       
    line = line + " values: " + str(A_int)
    entry.A_int = int(A_int)
    if B_int == None:
        B_int = 0   
    line = line + " values: " + str(B_int)
    entry.B_int = int(B_int)
    line = line + " values: " + str(A_str)
    entry.A_str = str(A_str)
    line = line + " values: " + str(B_str)
    entry.B_str = str(B_str)        
    line = line + " values: " + str(C_str)
    entry.C_str = str(C_str).replace("\n", "")
    line = line + " values: " + str(D_str)
    entry.D_str = str(D_str)
    line = line + " values: " + str(E_str)
    entry.E_str = str(E_str)
    line = line + " values: " + str(A_bool)
    entry.A_bool = bool(A_bool)
    line = line + " values: " + str(B_bool)
    entry.B_bool = bool(B_bool)
    line = line + " values: " + str(A_date)
    if type(A_date) == datetime:
        entry.A_date = A_date
    elif type(A_date) == str:
        x = str(A_date)
        z = datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S")
        dateFormated = z.replace(microsecond=int(x[20:]))
        entry.A_date = dateFormated
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def maketest(num, date):
    line = "Start-"
    x = Test()
    line = line + " values: " + str(num)
    x.num = int(num)
    line = line + " values: " + str(date)
    x.created = (date)       
    try:
        line = line + "put-sub-"
        x.put()
    except:
        return "sendData failure: " + line 
    line = "end"
    return "success"

def startGdataWB(variables):
    runStatus, workbook, stepNum = variables
    line = "Start-"
    entry = gdataDB()
    line = line + " values: " + str(runStatus)
    entry.runStatus = str(runStatus)
    line = line + " values: " + str(workbook)
    entry.workbook = str(workbook)
    line = line + " values: " + str(stepNum)
    entry.stepNum = int(stepNum)
    try:
        line = line + "put-sub-"
        entry.put()
    except:
        return "startGdataWB failure: " + line 
    line = "end"
    return "success"

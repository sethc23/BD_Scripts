'''
Created on Mar 21, 2009

@author: sethchase
'''
from queryData import checkVariable, getOneCategory, sendError
from queryData import getNewCategory, updateOneCategory, deleteRuntimeVar

def sendErrorApp(app):
    if app == "GetPostCount":
        # runtime variable
        appVariable = "runCateCount"
        checkPrevious = checkVariable(appVariable)
        if checkPrevious == False:
            section = getNewCategory()
            if str(section) == "Nothing to Update":
                return "counting schedule done"
            location = section.location
            category = section.category
            currentUrl = section.url
            # create error
            error = ("\n" + "no app variable, so here's the url: " + str(currentUrl) + "\n")
            string1 = str(location)
            string2 = str(category)
        else:
            action = checkPrevious.A_str
            currentCount = checkPrevious.A_int
            currentUrl = checkPrevious.B_str
            indexPost = checkPrevious.C_str
            toDate = checkPrevious.D_str
            fromDate = checkPrevious.E_str
            # get hierarchy data
            s = currentUrl.find(".org/") + 5
            e = currentUrl.find("/", s) + 1
            fullurl = currentUrl[:e]
            hierarchyVar = getOneCategory(fullurl)
            location = hierarchyVar.location
            category = hierarchyVar.category
            # create error
            error = ("\n" + "variable: " + str(appVariable) + "\n" + 
                     "action: " + str(action) + "\n" + 
                     "currentCount: " + str(currentCount) + "\n" + 
                     "currentUrl: " + str(currentUrl) + "\n" + 
                     "indexPost: " + str(indexPost) + "\n" + 
                     "toDate: " + str(toDate) + "\n" + 
                     "fromDate: " + str(fromDate) + "\n" + 
                     "fullurl: " + str(fullurl) + "\n")
            string1 = str(location)
            string2 = str(category)
        index, status = None, False
        # save combined data
        sendData = sendError(error, string1, string2, index, status)
        if str(sendData) != "success":
            return "error: sendError - sending error variable failed"
        # change DB to counted
        updated = updateOneCategory(location, category)
        if str(updated) != "Updated":
            return "error: sendError update hierarchy error"
        # delete runtime variable
        if checkPrevious != False:
            deleted = deleteRuntimeVar(appVariable)
            if str(deleted) != "variable deleted":
                return "error: sendError - deleting runtime variable failed"
        return "success"
    else:
        return "no app to handle error for"

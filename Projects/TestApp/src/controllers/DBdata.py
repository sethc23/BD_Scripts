'''
Created on Mar 16, 2009

@author: sethchase
'''

from queryData import checkVariable, getDBCount, sendVariable, deleteRuntimeVar, updateVariable

def runDBcount(database):
    appVariable = "DBcount"
    checkPrevious = checkVariable(appVariable)
    if checkPrevious == False:
        dbCount, lastDate = getDBCount(database, None)
        if str(dbCount).find("error") == 0:
            return "error: runDBcount-getDBCount", ""
        if dbCount == 0:
            return "complete", dbCount 
        else:
            if dbCount < 100 and lastDate == "":
                return "complete", dbCount 
            else:
                makeVariable = sendVariable(appVariable, dbCount, 0, None, None, None, None, None, None, None, lastDate)
                if str(makeVariable) != "success":
                    return "error: runDBcount-deleting variable", ""
                else:
                    return "run again - variable made", None
    else:
        currentDateIndex = str(checkPrevious.A_date)
        currentCount = checkPrevious.A_int
        newCount, lastDate = getDBCount(database, currentDateIndex)
        if str(newCount).find("error") == 0:
            return "error: runDBcount-getDBCount", ""
        if newCount == 0:
            deleted = deleteRuntimeVar(appVariable)
            if str(deleted) != "variable deleted":
                return "error: runDBcount-deleting variable", ""
            else:
                return "complete", currentCount
        else:
            dbCount = currentCount + newCount
            if lastDate == "":
                deleted = deleteRuntimeVar(appVariable)
                if str(deleted) != "variable deleted":
                    return "error: runDBcount-deleting variable", ""
                else:
                    return "complete", dbCount
            else:
                updated = updateVariable(appVariable, dbCount, 0, None, None, None, None, None, None, None, lastDate)
                if str(updated) != "Updated":
                    return "error: runDBcount-updating variable", ""
                else:
                    return "run again - variable updated" + str(lastDate), None

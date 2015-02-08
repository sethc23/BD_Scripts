'''
Created on Mar 16, 2009

@author: sethchase
'''

from DBdata import runDBcount
from time import time

def DBdataApp(self, action, variable):
    if action == "count":
        database = variable
        now = int(time())
        end = now + (25)
        complete = False
        attempts = 5
        while end >= now and attempts != 0:
            status, dbCount = runDBcount(database)
            if status == "complete":
                complete = True
                break
            now = int(time())
            attempts = attempts - 1
        if complete == True:
            return dbCount
        else:
            return "run again"        
    else:
        # allow option to make query, show results and count
        return "error: no action sent"
        # pass

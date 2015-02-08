import os
from appscript import *
from time import sleep
from sys import path
from datetime import datetime
path.append('/Users/admin/SERVER2/BD_Scripts/utility')

# terminal = app(u'Terminal')
# terminalProcess = app(u'System Events').processes['Terminal']
# pyShell = app(u'System Events').processes[u'IDLE'].windows[u'Python Shell']

def setupTermWin():
    app(u'Terminal').activate()
    # print app(u'Terminal').windows[1].bounds.get()
    try:
        f = open('/Users/admin/Work/ScanBusiness/Clients/UNH/Bayh-Dole/logs/macPrefs.txt', 'r')
        x = f.readlines()
        f.close()
        for it in x:
            if it.split(':')[0] == 'terminal': 
                app(u'Terminal').windows[1].bounds.set(eval(it.split(':')[1]))
                break
    except:
        app(u'Terminal').windows[1].bounds.set([1055, 22, 1867, 624])

def getTerminalHistory():
    t = datetime.now()
    a = t.strftime('%Y.%m.%d_%H:%M:%S')
    b = app(u'Terminal').windows[1].tabs[1].history.get()
    return a, b

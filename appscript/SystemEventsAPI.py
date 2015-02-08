from appscript import *
import os, osax
from datetime import date
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
#import sortListArray, listFout, listFin

def keys(keyType, var, modifier=''):
    cmd = """osascript -e 'tell app "System Events" to """
    var = unicode(var).encode('ascii', 'ignore')
    if keyType == 'keycode':
        cmd += "key code "
        cmd += str(var)
    elif keyType == 'keystroke':
        cmd += "keystroke "
        cmd += '"' + str(var) + '"'
    else:
        print 'invalid key type in SystemEventsKey'
    if modifier != '':
        if type(modifier) == str:
            cmd += " using " + modifier
        elif type(modifier) == list:
            cmd += " using {"
            for it in modifier:
                cmd += it + ','
            cmd = cmd.rstrip(',')
            cmd += "}"
    cmd += "'"
    # print cmd
    os.system(cmd)

"""
def WordCmd(cmd,var=''):
    app(u'Microsoft Word').activate()
    if cmd=='copy':
        SystemEventsKeys('keycode',8,'command down')
    elif cmd=='paste':
        SystemEventsKeys('keycode',9,'command down')
    elif cmd=='delete':
        SystemEventsKeys('keycode',117,'command down')
    elif cmd=='backspace':
        SystemEventsKeys('keycode',51,'command down')
    elif cmd=='end':
        SystemEventsKeys('keycode',119)
    elif cmd=='endofdoc':
        SystemEventsKeys('keycode',119,'option down')
    elif cmd=='return':
        SystemEventsKeys('keycode',36)
    elif cmd=='singlequote':
        SystemEventsKeys('keycode',39)
    elif cmd=='doublequote':
        SystemEventsKeys('keycode',39,'shift down')
    elif cmd=='uparrow':
        SystemEventsKeys('keycode',126)
    elif cmd=='downarrow':
        SystemEventsKeys('keycode',125)
    elif cmd=='leftarrow':
        SystemEventsKeys('keycode',123)
    elif cmd=='rightarrow':
        SystemEventsKeys('keycode',124)
    elif cmd=='leftoneword':
        SystemEventsKeys('keycode',123,'option down')
    elif cmd=='rightoneword':
        SystemEventsKeys('keycode',124,'option down')
    elif cmd=='type':
        #SystemEventsKeys('keystroke',var)
        if var.find('"') == -1 and var.find("'") == -1:
            SystemEventsKeys('keystroke',var)
        else:
            var=var.replace('"','\\"')
            if var.find("'") == -1:
                SystemEventsKeys('keystroke',var)
            else:
                a=var.split("'")
                last=False
                for i in range(0,len(a)):
                    if a[i] == '':
                        SystemEventsKeys('keycode',39)
                        last=True
                    elif a[i] != '':
                        if last==False:
                            SystemEventsKeys('keystroke',a[i])
                            if i != len(a)-1:
                                SystemEventsKeys('keycode',39)
                                last=True
                        else:
                            SystemEventsKeys('keystroke',a[i])
                            if i != len(a)-1:
                                SystemEventsKeys('keycode',39)
                                last=True
                            else:
                                last=False
    elif cmd=='rightindent':
        SystemEventsKeys('keycode',124,['control down','shift down'])
    elif cmd=='leftindent':
        SystemEventsKeys('keycode',123,['control down','shift down'])
    elif cmd=='selectaboveparagraph':
        SystemEventsKeys('keycode',126,['command down','shift down'])
    elif cmd=='selectbelowparagraph':
        SystemEventsKeys('keycode',125,['command down','shift down'])

"""

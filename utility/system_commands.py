from appscript import *
import os, osax
from datetime import date
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
import sortListArray, listFout, listFin

def copy(txt):
    # txt=unicode(txt).encode('ascii','replace')
    os.system('echo "' + txt + '" | pbcopy')

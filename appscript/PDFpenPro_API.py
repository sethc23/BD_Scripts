import os
from appscript import *
from time import sleep
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from SortStringListByLength import *

adobe = app(u'PDFpenPro')
adobeProcess = app(u'System Events').processes[u'Acrobat']
pyShell = app(u'System Events').processes[u'IDLE'].windows[u'Python Shell']

def openPDF(filePath):
    app(u'PDFpenPro').activate()
    app(u'PDFpenPro').open(filePath)

def closeWindow():
    app(u'PDFpenPro').documents[1].close(saving=k.no)

def getPageWidth(pgNum=''):
    app(u'PDFpenPro').activate()
    if pgNum == '': return app(u'PDFpenPro').documents[1].pages.width.get()
    else: return app(u'PDFpenPro').documents[1].pages[pgNum].width.get()

def getPageHeight(pgNum=''):
    app(u'PDFpenPro').activate()
    if pgNum == '': return app(u'PDFpenPro').documents[1].pages.height.get()
    else: return app(u'PDFpenPro').documents[1].pages[pgNum].height.get()

from appscript import *
from time import sleep
import sys

def printMenu(processName, printPerPage, button_num):
    # print processName
    # print button_num
    printer = app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].value.get()
    # printer=app(u'System Events').processes[u'Microsoft Word'].windows[u'Print'].pop_up_buttons[3].value.get()
    print '1'
    if printer != "CUPS-PDF_BW":
        app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
        app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'CUPS-PDF_BW'].click()
    button_num = button_num - 1
    printerSetting = app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].value.get()
    print '2'
    if printerSetting != "Standard-1":
        if printPerPage == "4":
            if printerSetting != "2_sided__4_pg":
                app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
                app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'2_sided__4_pg'].click()
        else:
            app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
            app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'Standard-1'].click()
    print '3'
    app(u'System Events').processes[processName].windows[u'Print'].buttons[u'Print'].click()
    

def pptPrint(fileOpen, printPerPage, fileSave):
    appName = 'Microsoft PowerPoint'
    processName = 'Microsoft PowerPoint'
    app(appName).activate()
    app(appName).open(fileOpen)
    app(appName).activate(timeout=36000)
    # sleep(2)
    app(appName).activate()
    # sleep(2)
    app(u'System Events').processes[processName].key_code(35, using=[k.command_down])
    sleep(0.50)
    printMenu(processName, printPerPage, 6)


def wordPrint(fileOpen, printPerPage, fileSave):
    appName = 'Microsoft Word'
    processName = appName
    app(appName).activate()
    app(appName).open(fileOpen)
    app(u'System Events').processes[processName].key_code(35, using=[k.command_down])
    printMenu(processName, printPerPage, 3)
    app(u'Microsoft Word').activate(timeout=36000)
    app(u'Microsoft Word').documents[1].close()

if __name__ == '__main__':
    
    #app(u'Finder').activate()
    #files = app(u'Finder').selection.get()
    #fileNames, fileTypes, filePaths = [], [], []
    
    for arg in sys.argv:
        printPerPage = arg
        print printPerPage
    
    for item in files:
        item = str(item)
        fileNames.append(item[item.rfind('[') + 3:item.rfind('[') + item[item.rfind('['):].find('.')])
        fileTypes.append(item[item.rfind('.') + 1:item.rfind("'")])
        path = '/'
        for part in item.split('folders[u'):
            if part[0] == "'":
                path = path + part[1:part[2:].find("'") + 2] + '/'
        filePaths.append(path)
    
    for i in range(0, len(fileNames)):
        fileOpen = filePaths[i] + fileNames[i] + "." + fileTypes[i]
        fileSave = fileNames[i] + '.pdf'
        if fileTypes[i] == "ppt":
            pptPrint(fileOpen, printPerPage, fileSave)
        elif fileTypes[i] == "doc" or fileTypes[i] == "docx":
            wordPrint(fileOpen, printPerPage, fileSave)
    


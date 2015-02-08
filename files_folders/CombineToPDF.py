from appscript import *
from time import sleep, time
import sys, os

def startAcrobat():
    app(u'Adobe Acrobat Professional').activate()

def quitAcrobat():
    app(u'Adobe Acrobat Professional').quit() 

def doScript(x):
    app(u'Adobe Acrobat Professional').activate()
    app(u'Adobe Acrobat Professional').do_script(x)

def doScriptReturn(x):
    app(u'Adobe Acrobat Professional').activate()
    return app(u'Adobe Acrobat Professional').do_script(x)

def newPDF():
    script = ('var myDoc = app.newDoc();')
    doScript(script)

def openFile(fileName):
    script = (
     'var filePath = "' + fileName + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function openPDF(filePath){' + 
     'try {' + 
     'app.openDoc({ ' + 
     'cPath: filePath, ' + 
     'bUseConv: true ' + 
     '})' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'openPDF(filePath);')
    doScript(script)

def closePDF():
    script = ('this.closeDoc(true);')
    doScript(script)

def insertPages(filePath):
    script = (
     'var filePath = "' + filePath + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function insertThis(filePath){' + 
     'try {' + 
     'this.insertPages({' + 
     'cPath: filePath' + 
     '});' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'insertThis(filePath);')
    doScript(script)

def deleteFirstPage():
    script = ('this.deletePages({});')
    doScript(script)

def renamePDF(filePath):
    script = ('var filePath = "' + filePath + '";' + 
     'function displayError(x){' + 
     'app.alert({' + 
     'cMsg: "Error! Try again! " + x,' + 
     'cTitle: "Acme Testing Service"' + 
     '});' + 
     '}' + 
     'function saveas(filePath){' + 
     'try {' + 
     'this.saveAs(filePath' + 
     ');' + 
     '} catch (e) { displayError(e); }' + 
     '}' + 
     'saveas(filePath);')
    doScript(script)

def combinePDFs(fileNames, fileTypes, filePaths, savePath):
    startAcrobat()
    sleep(1.5)
    try:
        app(u'System Events').processes[u'Acrobat'].windows[1].buttons[u'No'].click()
    except:
        pass
    sleep(.5)
    newPDF()
    printedName, modName = [], []
    days20ago = int(time.time()) - 20 * (24 * 60 * 60)
    for item in printedList:
        if item != '.DS_Store':
            if os.stat(printerPath + item)[ST_MTIME] >= days20ago:
                printedName.append(item)
                modName.append(item[item.find('-') + 1:])
            else:
                cmd = 'rm ' + printerPath + item
                os.system(cmd)
    for i in range(0, len(fileNames)):
        modOpen = filePaths[i] + fileNames[i] + "." + fileTypes[i]
        fileOpen = printedName[modName.index(modOpen)]
        fileSave = fileNames[i] + '.pdf'
        insertPages(fileOpen)
    deleteFirstPage()
    renamePDF(savePath)
    closePDF()
    quitAcrobat()

def convertToPDF(fileNames, fileTypes, filePaths, args):
    printPerPage = args[0]
    printerPath = '/var/spool/cups-pdf/admin/'
    printedList = os.listdir(printerPath)
    for i in range(0, len(fileNames)):
        if fileTypes[i].lower() != "pdf":
            fileSave = fileNames[i].replace(' ', '_').replace('.', '_') + '.pdf'
            fileOpen = filePaths[i] + fileNames[i] + "." + fileTypes[i]
            if fileTypes[i] == "ppt":
                pptPrint(fileOpen, printPerPage, fileSave)
            elif fileTypes[i] == "doc" or fileTypes[i] == "docx":
                wordPrint(fileOpen, printPerPage, fileSave)
                if fileTypes[i] == "docx":
                    fileSave = 'Microsoft_Word_-_' + fileSave[:-4] + '_docx' + '.pdf'
                else:
                    fileSave = 'Microsoft_Word_-_' + fileSave
            fileOpen = filePaths.pop(i) + fileNames.pop(i) + "." + fileTypes.pop(i)
            filePaths.insert(i, printerPath)
            fileNames.insert(i, fileSave[:-4])
            fileTypes.insert(i, 'pdf')
    x = app(u'System Events').processes.name.get()
    y = ['Microsoft Word', 'Microsoft Powerpoint']
    for item in x:
        if str(y).find(item) != -1:
            app(item).quit()
    return fileNames, fileTypes, filePaths

def printMenu(processName, printPerPage, button_num):
    sleep(1.5)
    printer = app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].value.get()
    sleep(1)
    if printer != "CUPS-PDF_BW":
        app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
        sleep(1)
        app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'CUPS-PDF_BW'].click()
        sleep(1)
    button_num = button_num - 1
    printerSetting = app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].value.get()
    sleep(1)
    if printerSetting != "Standard-1":
        if printPerPage == "4":
            if printerSetting != "2_sided__4_pg":
                app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
                sleep(1)
                app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'2_sided__4_pg'].click()
                sleep(1)
        else:
            app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].click()
            sleep(1)
            app(u'System Events').processes[processName].windows[u'Print'].pop_up_buttons[button_num].menus[1].menu_items[u'Standard-1'].click()
            sleep(1)
    app(u'System Events').processes[processName].windows[u'Print'].buttons[u'Print'].click()
    sleep(1.5)

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
    

app(u'Finder').activate()
files = app(u'Finder').selection.get()
fileNames, fileTypes, filePaths = [], [], []

try:
    args = []
    for a in sys.argv:
        args.append(a)
except:
    args.append('')

for item in files:
    item = str(item)
    fileNames.append(item[item.rfind('[') + 3:item.rfind('[') + item[item.rfind('['):].find('.')])
    fileTypes.append(item[item.rfind('.') + 1:item.rfind("'")])
    path = '/'
    for part in item.split('folders[u'):
        if part[0] == "'":
            path = path + part[1:part[2:].find("'") + 2] + '/'
    filePaths.append(path)

origPath = filePaths[0]
saveName = origPath[origPath.rfind('/', 0, origPath.rfind('/') - 1) + 1:-1]
savePath = origPath + saveName + '.pdf'

fileNames, fileTypes, filePaths = convertToPDF(fileNames, fileTypes, filePaths, args)

combinePDFs(fileNames, fileTypes, filePaths, savePath)

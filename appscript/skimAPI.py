from appscript import *

def activate():
    app(u'Skim').activate()

def openPDF(filePath):
    filePath = filePath.replace('/', ':')
    if filePath[0] == '/':
        filePath = filePath[1:]
    app(u'Skim').activate()
    app(u'Skim').open(filePath)

def closePDF(document):
    app(u'Skim').activate()
    app(u'Skim').documents[document].close()

def getSkimWindow():
    app(u'Skim').activate()    
    return app(u'Skim').windows[1].bounds.get()

def setSkimWindow(position):  # =[176, 22, 1111, 632]
    app(u'Skim').activate()    
    app(u'Skim').windows[1].bounds.set(position)

def setSkimWindowLeft():
    app(u'Skim').activate()    
    app(u'Skim').windows[1].bounds.set([5, 22, 718, 900])

def getNotes(openFile):
    app(u'Skim').activate()
    return app(u'Skim').documents[openFile].notes.get()

def copy_page_text():
    app(u'Skim').activate()
    app(u'System Events').processes[u'Skim'].menu_bars[1].menu_bar_items[u'PDF'].menus[1].menu_items[u'PDF Display'].menus[1].menu_items[u'Single Page'].click()
    app(u'System Events').processes[u'Skim'].key_code(24, using=k.command_down)
    app(u'Skim').activate()
    app(u'System Events').processes[u'Skim'].keystroke(u'c', using=k.command_down)

from appscript import *
import os, osax
from time import sleep
from datetime import date
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
#import sortListArray, listFout, listFin
from SystemEventsAPI import keys


def openWordFile(path):
    app(u'Microsoft Word').activate()
    app(u'Microsoft Word').open(path)

def saveAs(filePath):
    script='expression.SaveAs("'+filePath+'")'
    

def activate():
    app(u'Microsoft Word').activate()

def makeFront(window):
    activate()
    sleep(1)
    app(u'System Events').processes[u'Microsoft Word'].frontmost.set(True)
    app(u'System Events').processes[u'Microsoft Word'].windows[its.title == window].actions[u'AXRaise'].perform()

def getWordWindow():
    app(u'Microsoft Word').activate()    
    return app(u'Microsoft Word').windows[1].bounds.get()

def setWordWindow(window):
    app(u'Microsoft Word').activate()    
    app(u'Microsoft Word').windows[1].bounds.set(window)

def VB_replace(old,new):
    app(u'Microsoft Word').activate()
    script=('With Selection.Find'+
        '.Text = "'+str(old)+'"'+
        '.Replacement.Text = "'+str(new)+'"'+
        '.Forward = True'+
        '.Wrap = False'+
        '.Format = False'+
        '.MatchCase = False'+
        '.MatchWholeWord = False'+
        '.MatchWildcards = False'+
        '.MatchSoundsLike = False'+
        '.MatchAllWordForms = False'+
    'End With')
    app(u'Microsoft Word').evaluate(script)  #NOT WORK DUE TO 2011 CHANGES

def replace(old,new):
    app(u'Microsoft Word').activate()
    app(u'Microsoft Word').selection.find_object.get()
    app(u'Microsoft Word').selection.find_object.content.set(old)
    app(u'Microsoft Word').selection.find_object.replacement.content.set(new)
    app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)

def WordCmd(cmd, var=''):
    app(u'Microsoft Word').activate()
    if cmd == 'copy':
        keys('keycode', 8, 'command down')
    elif cmd == 'paste':
        keys('keycode', 9, 'command down')
    elif cmd == 'selectall':
        keys('keycode', 0, 'command down')
    elif cmd == 'delete':
        keys('keycode', 117, 'command down')
    elif cmd == 'backspace':
        keys('keycode', 51, 'command down')
    elif cmd == 'end':
        keys('keycode', 119)
    elif cmd == 'endofdoc':
        keys('keycode', 119, 'option down')
    elif cmd == 'return':
        keys('keycode', 36)
    elif cmd == 'singlequote':
        keys('keycode', 39)
    elif cmd == 'doublequote':
        keys('keycode', 39, 'shift down')
    elif cmd == 'uparrow':
        keys('keycode', 126)
    elif cmd == 'downarrow':
        keys('keycode', 125)
    elif cmd == 'leftarrow':
        keys('keycode', 123)
    elif cmd == 'rightarrow':
        keys('keycode', 124)
    elif cmd == 'leftoneword':
        keys('keycode', 123, 'option down')
    elif cmd == 'rightoneword':
        keys('keycode', 124, 'option down')
    elif cmd == 'type':
        # SystemEventsKeys('keystroke',var)
        if var.find('"') == -1 and var.find("'") == -1:
            keys('keystroke', var)
        else:
            var = var.replace('"', '\\"')
            if var.find("'") == -1:
                keys('keystroke', var)
            else:
                a = var.split("'")
                last = False
                for i in range(0, len(a)):
                    if a[i] == '':
                        keys('keycode', 39)
                        last = True
                    elif a[i] != '':
                        if last == False:
                            keys('keystroke', a[i])
                            if i != len(a) - 1:
                                keys('keycode', 39)
                                last = True
                        else:
                            keys('keystroke', a[i])
                            if i != len(a) - 1:
                                keys('keycode', 39)
                                last = True
                            else:
                                last = False
    elif cmd == 'rightindent':
        keys('keycode', 124, ['control down', 'shift down'])
    elif cmd == 'leftindent':
        keys('keycode', 123, ['control down', 'shift down'])
    elif cmd == 'selectaboveparagraph':
        keys('keycode', 126, ['command down', 'shift down'])
    elif cmd == 'selectbelowparagraph':
        keys('keycode', 125, ['command down', 'shift down'])

def Word_getIndent():
    app(u'Microsoft Word').activate()
    # app(u'Microsoft Word').selection.set(k.null)
    app(u'Microsoft Word').selection.get()
    app(u'Microsoft Word').selection.properties.get()
    app(u'Microsoft Word').selection.paragraphs[1].get()
    app(u'Microsoft Word').selection.paragraphs[1].paragraph_format.get()
    x = app(u'Microsoft Word').selection.paragraphs[1].paragraph_format.properties.get()
    """
    a=x.iterkeys()
    b=x.itervalues()
    iterVals=[],[]
    for it in a:
        iterVals[0].append(it)
    for it in b:
        iterVals[1].append(it)
    for i in range(0,len(iterVals[0])):
        print iterVals[1][i],'  =  ',iterVals[0][i]
    """
    keys = x.keys()
    values = x.values()
    bottom_slider, top_slider = '', ''
    for it in keys:
        if str(it) == "k.first_line_indent":  # top slider indent
            i_num = keys.index(it)
            top_slider = values[i_num]
        if str(it) == "k.paragraph_format_left_indent":  # bottom slider indent
            i_num = keys.index(it)
            bottom_slider = values[i_num]

        if bottom_slider != '' and top_slider != '':
            return top_slider, bottom_slider

def getWordFormats():
    return ['bold', 'italic', 'underline', 'caps', 'size', '(plain)']

def clearFormats():
    app(u'Microsoft Word').activate()
    app(u'Microsoft Word').selection.get()
    app(u'Microsoft Word').selection.clear_formatting()
    return 'success'

def formatText(find_txt, repl_txt, format, var=''):
    if type(format) == str:
        format = [format]
    if var == '(none)':
        return 'pass'    
    app(u'Microsoft Word').activate()
    app(u'Microsoft Word').selection.find_object.get()
    # app(u'Microsoft Word').selection.find_object.clear_formatting()
    try:
        app(u'Microsoft Word').selection.find_object.content.set(find_txt)
        app(u'Microsoft Word').selection.find_object.replacement.clear_formatting()
        app(u'Microsoft Word').selection.find_object.replacement.content.set(repl_txt)
    except:
        WordCmd('type', repl_txt)
        WordCmd('selectaboveparagraph')
        app(u'Microsoft Word').selection.find_object.replacement.get()
        format_var = format, var
        selectedText(format_var)
        return 'success'
    # print 'success'
    if format.count('bold') != 0:
        app(u'Microsoft Word').selection.find_object.replacement.font_object.bold.set(True)
        app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)
    if format.count('underline') != 0:
        app(u'Microsoft Word').selection.find_object.replacement.font_object.underline.set(True)
        app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)
    if format.count('italic') != 0:
        app(u'Microsoft Word').selection.find_object.replacement.font_object.italic.set(True)
        app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)
    if format.count('size') != 0:
        app(u'Microsoft Word').selection.find_object.replacement.font_object.font_size.set(str(var))
        app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)
    if format.count('caps') != 0:
        app(u'Microsoft Word').selection.find_object.replacement.font_object.all_caps.set(True)  
        app(u'Microsoft Word').selection.find_object.execute_find(match_forward=True, wrap_find=k.find_continue, match_whole_word=True, match_case=False, replace=k.replace_all)
    return 'success'

def selectedText(format_var):
    if type(format_var) == list or type(format_var) == tuple: format, var = format_var
    elif type(format_var) == str: format = format_var
    try:
        if type(format) == str: format = [format]
    except:
        print type(format_var), type(format), type(it)
        print asdsa
    for it in format:
        it = it.lower()
        if it == 'bold':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.bold.set(True) 
        if it == 'underline':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.underline.set(True) 
        if it == 'italic':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.italic.set(True) 
        if it == 'size':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.font_size.set(str(var))
        if it == 'caps':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.all_caps.set(True)
        if it == '(plain)':
            app(u'Microsoft Word').selection.get()
            app(u'Microsoft Word').selection.font_object.bold.set(False)
            app(u'Microsoft Word').selection.font_object.underline.set(False)
            app(u'Microsoft Word').selection.font_object.italic.set(False)
            app(u'Microsoft Word').selection.font_object.font_size.set(str('12'))
            app(u'Microsoft Word').selection.font_object.all_caps.set(False)



f=open('/Users/admin/Desktop/round1.txt','r')
x=f.readlines()
f.close()
#print len(x)
#print adf
template='NOSJM-template.docx'
goto='NOSJM-1.docx'

'''
i=0
c=x[i].split('\t')
plaintiff=c[4]
index=c[2]
firm=c[5].strip('\r\n')

makeFront(template)
sleep(1)
WordCmd('selectall', var='')
sleep(1)
WordCmd('copy', var='')
sleep(1)
makeFront(goto)
WordCmd('paste', var='')
sleep(1)
replace('#PLAINTIFF#',plaintiff)
replace('#INDEX#',index)
replace('#FIRM#',firm)
WordCmd('endofdoc', var='')
'''

for i in range(151,len(x)):
    c=x[i].split('\t')
    index=c[3]
    plaintiff=c[2]
    firm=c[5].strip('\r\n')
    if firm == "Wilentz, Goldman & Spitzer":
        firmstreet='110 William Street, 26th Floor'
        firmcity='New York, NY  10038'
        firmphone='(212) 267-3091'
    elif firm == "Weitz & Luxenberg":
        firmstreet='700 Broadway'
        firmcity='New York, NY  10003'
        firmphone='(212) 558-5500'
    elif firm == "Early & Strauss":
        firmstreet='360 Lexington Avenue, 20th Fl.'
        firmcity='New York, NY  10017'
        firmphone='(212) 986-2233'
    else:
        print c  
    #print len(x)
    #print c
    #print asdfds
    #if plaintiff.lower().count(str('PREVIDI').lower()) != 0:
    #    print i,' of ',firm

    #'''
    if i==151:
        activate()
        makeFront(template)
        sleep(1)
        WordCmd('selectall', var='')
        sleep(1)
        WordCmd('copy', var='')
        sleep(1)
        makeFront(goto)
    WordCmd('paste', var='')
    sleep(1)
    replace('#PLAINTIFF#',plaintiff)
    replace('#INDEX#',index)
    replace('#FIRM#',firm)
    replace('#FIRMSTREET#',firmstreet)
    replace('#FIRMCITY#',firmcity)
    replace('#FIRMPHONE#',firmphone)
    WordCmd('endofdoc', var='')
    #break
    #'''

#c=x[0].split('\t')[len(x[0].split('\t'))-1]
#print len(c.strip('\r\n'))
#print len('Wilentz Goldman and Spitzer')
#replace("#MONTH#",'today')
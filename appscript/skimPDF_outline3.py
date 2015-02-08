from appscript import *
import os, osax
from datetime import date
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
import sortListArray, listFout, listFin
from system_commands import copy
from SystemEvents import SystemEventsKeys
from pyDialog import askQuestion, multiQuestion
from Word_API import openWordFile, WordCmd, Word_getIndent
from Word_API import formatText, getWordFormats, selectedText, clearFormats

def genericOutline():
    print ""
    print "What section of outline:"
    print ""
    print "1 -- ", "1."
    print "2 -- ", " .01"
    print "3 -- ", "     A."
    print "4 -- ", "         1."
    print "5 -- ", "             a."
    print "6 -- ", "                 i."
    print ""

def genericStyles():
    print ""
    print "n -- ", '(default is "a,g")'
    print ''
    print 'or make new combination with:'
    print ''
    print "a -- ", "Normal"
    print "b -- ", "Bold"
    print "c -- ", "Underline"
    print "d -- ", "All Caps"
    print "e -- ", "Double Underline"
    print "f -- ", "Size 10"
    print "g -- ", "Size 12"
    print "h -- ", "Size 14"
    print "i -- ", "Size 16"
    print "j -- ", "Size 18"
    print ""

def getConditions():
    # conditions = type_colors,text
    conditions = [
                [['type_colors', 'text'],
                 ['k.underline_note:black', ' v. '],
                 'Start special "case outline" when a black underline contains the text " v. " '],

            
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:yellow', '<U><B>PROC. HIST.</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:pink', '<U><B>CLAIMS</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:light_green', '<U><B>ISSUE</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:purple', '<U><B>FACTS</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:dark_blue', '<U><B>REASONING</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:orange', '<U><B>LAW</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                [['type_colors', 'text', 'type_colors', 'text'],
                 ['k.underline_note:black', ' v. ', 'k.underline_note:red', '<U><B>HOLDING</B></U>'],
                 'Conditioned on k.underline_note:black having text " v. " '],
                
                [['type_colors'],
                 ['k.underline_note:dark_green'],
                 'This is used to add text to the previous underline in the case where the underline extends to next page'],
                [['type_colors'],
                 ['k.underline_note:light_blue'],
                 'This is used to indent text under last underline. Applies for any color.'],
                [['type_colors'],
                 ['k.underline_note:grey'],
                 'This is used to identify the source of a nearby underline and include the reference in relevant underlined text.'],
                [['type_colors'],
                 ['k.highlight_note:orange'],
                 'This highlight will bold the highlight, add an " = " to the end, and adjoin the closest underline of the text (or if closest note based on audibles "ABOVE" and "BELOW")']
                 ]

    return conditions

def getSpecialTreatment():
    special_treatment = ['k.underline_note:dark_green',
                         'k.underline_note:grey']
    return special_treatment

def getSpecialContext():
    special_context = ['k.underline_note:lite_blue',
                       'k.highlight_note:orange']
    return special_context

def closestNote(data, i):
    if data[3][i].find('BELOW') or data[3][i].find('ABOVE'):
        if data[3][i].find('BELOW'):
            prevDist, nextDist = 2, 1
            data[3][i] = data[3][i].replace('BELOW', '')
        elif data[3][i].find('ABOVE'):
            prevDist, nextDist = 1, 2
            data[3][i] = data[3][i].replace('ABOVE', '')
    else:
        a = data[4][i - 1]
        a_e = a[len(a) - 1][a[len(a) - 1].find(':') + 1:]
        b = data[4][i]
        b_s = b[0][:b[0].find(':')]
        b_e = b[len(b) - 1][b[len(b) - 1].find(':') + 1:]
        c = data[4][i + 1]
        c_s = c[0][:b[0].find(':')]
        prevDist = eval(b_s.strip(':')) - eval(a_e.strip(':'))
        nextDist = eval(c_s.strip(':')) - eval(b_e.strip(':'))
        if prevDist == nextDist:
            prevText, nextText = 2, 1
    # prevText < nextText: = meaning: closest underlined text is BEFORE this underline
    # prevText > nextText: = meaning: closest underlined text is AFTER this underline
    return prevDist, nextDist

def printNote(text):
    if len(text) > 30:
        pt = 0
        x = int(round(len(text) / 30.0, 0)) + 1
        print 'num=', x
        for i in range(0, x):
            y = text[pt:pt + 30]
            e = y.rfind(' ')
            print text[pt:e]
            pt = pt + e
    else:
        print text

def skim_PageCharacters(var):
    start = 'text.characters['
    if type(var) == list:
        char_range = []
        for it in var:
            it = str(it)
            if len(it.split(start)) != 4:
                pass
            else:
                c = it.rfind(start) + len(start)
                d = it.find(']', c)
                a = it[:c - len(start)].rfind(start) + len(start)
                b = it.find(']', a)
                x = str(it[a:b] + ':' + it[c:d])
                if x.replace(':', '').isdigit() == False:
                    print 'error with skim_PageCharacters'
                    print ''
                    print var
                    print ''
                    print it
                    print ''
                    print x
                    print ''
                    return
                char_range.append(str(it[a:b] + ':' + it[c:d]))
    else:
        it = str(var)
        a = it.find(start) + len(start)
        b = it.find(']', a)
        c = it.find(start, b) + len(start)
        d = it.find(']', c)
        char_range = str(it[a:b] + ':' + it[c:d])
    return char_range

def updateColors(color_vars, uniq_category, data):
    skim_colors, used_colors, add_colors = color_vars
    reviewed = []
    # data = type[0],page,color[2],text,charRange[4]
    for it in add_colors:
        s = data[2].index(it)
        stop = False
        while stop == False:
            print ''
            print 'On page ' + data[1][s] + ', What is the note color of the following text:'
            print ''
            print '\t' + data[3][s]
            print ''
            new_color = raw_input(":")
            step = askQuestion('Is "' + new_color + '" correct?', "(y/n)?", ['y', 'n'])
            if step == 'y':
                stop = True
        skim_colors.append((new_color, it))
        pt = 0
        for j in range(0, data[2].count(it)):
            i_num = data[2].index(it, pt)
            pt = i_num + 1
            data[2][i_num] = new_color
            
            type_color = str(data[0][i_num]) + ':' + str(new_color)
            if uniq_category.count(type_color) == 0:
                uniq_category.append(type_color)

    listFout.listFout(skim_colors, 'skim_colors.txt')
    return data, skim_colors, uniq_category

def getNotesFromSkim(data, openFile):
    # -- get note data
    docNotes = app(u'Skim').documents[openFile].notes.get()
    noteCount = len(docNotes)
    add_colors, used_colors = [], []
    checkColors = False
    try:
        skim_colors = listFin.listFin('skim_colors.txt')
    except:
        # skim_colors,skim_types=skimVars()
        skim_colors = []
        checkColors = True
        print 'fail'

    uniq_category, uniq_page = [], []
    for note in docNotes:
        a = note.type()
        if str(a) == 'k.underline_note' or str(a) == 'k.highlight_note':
            data[0].append(str(a))
            b = eval(str(note.page.index()))
            data[1].append(b)
            data[3].append(note.text.get())
            var = note.selection.get()  
            data[4].append(skim_PageCharacters(var))

            if [v for k, v in skim_colors].count(note.color.get()) == 0:
                data[2].append(note.color.get())
                if add_colors.count(note.color.get()) == 0:
                    add_colors.append(note.color.get())
                    # print 'fail2',note.color.get()
                checkColors = True
                
            else:
                c = skim_colors[[v for k, v in skim_colors].index(note.color.get())][0]
                data[2].append(str(c))
                if used_colors.count(str(c)) == 0:
                    used_colors.append(str(c))
                    
                type_color = str(a) + ':' + str(c)
                if uniq_category.count(type_color) == 0:
                    uniq_category.append(type_color)
                    
            if uniq_page.count(b) == 0:
                uniq_page.append(b)

    if checkColors == True:
        print 'Not all colors are recognized by this program.'
        print 'Please review the following', len(add_colors), 'questions.'
        print ''
        color_vars = skim_colors, used_colors, add_colors
        data, skim_colors, uniq_category = updateColors(color_vars, uniq_category, data)

    return data, uniq_category, uniq_page, skim_colors

def reOrderNotes(data, uniq_page):
    #--- re-order notes according to page and characters
    c = data
    data = sortListArray.sortListArray(c, 1)
    data_pages, data_ranges = list(data[1]), list(data[4])
    same_page_ranges, sorted_page_ranges = [], []
    # sorted_data = page_num, data_row
    sorted_data = [], []
    for page in uniq_page:
        if data_pages.count(page) != 1:  # if data has more than one note on a page
            a = data_pages.index(page)  # determine range in data having same page number
            data_pages.reverse()
            b = len(data_pages) - data_pages.index(page)
            data_pages.reverse()
            chars = [], [], []  # [page,data index, char]
            for i in range(a, b):  # in the range with same page number, determine what the first char is 
                x = data[4][i]
                a2 = x[0][:x[0].find(':')]
                chars[0].append(page)
                chars[1].append(i)
                chars[2].append(eval(str(a2)))
            pt = 0
            for it in chars[2]:
                x = it
                if x > pt:
                    pt = x
                else:
                    chars = sortListArray.sortListArray(chars, 2)  # sort (range with same page number) by first char
                    if chars[2][0] > chars[2][len(chars[2]) - 1]:
                        chars = sortListArray.sortListArray(chars, 2)  # re-sort if backwards
                    for j in range(0, len(chars[0])):  # make new list (sorted by first char) having page number and data
                        sorted_data[0].append(chars[0][j])
                        temp = []
                        for k in range(0, len(data)):
                            temp.append(data[k][chars[1][j]])
                        sorted_data[1].append(temp)
                    break
    new_data = []
    for it in data:
        new_data.append([])
    for i in range(0, len(data[0])):  # make new data list substituting (pages ordered by char) with (pages not ordered by char)
        page = data[1][i]
        if sorted_data[0].count(page) == 0:
            for j in range(0, len(data)):
                new_data[j].append(data[j][i])
        else:
            i_num = sorted_data[0].index(page)
            junk = sorted_data[0].pop(i_num)
            if junk != page:
                print 'error: sortedData page != data page', junk, ' != ', page
            new_part = sorted_data[1].pop(i_num)
            for j in range(0, len(data)):
                new_data[j].append(new_part[j])  
    if len(data[0]) != len(new_data[0]):
        print 'error: len(data[0]) != len(new_data[0])'
    data = new_data
    return data

def customOutline(structure, uniq_category, level_refs):
    print ''
    print 'Current settings for outline are:'
    print ''
    print 'Level:\t\t\tIndex \tNoteType:Color:'
    print '---------------------------------------'
    special_treatment = getSpecialTreatment()
    special_context = getSpecialContext()
    if structure[0] != []:
        a = list(structure[0:3])
        b = sortListArray.sortListArray(a, 2)
        c = [str(b[0][i]) + ':' + str(b[1][i]) for i in range(0, len(b[0]))]
        d = [], [], []
        for it in uniq_category:
            if c.count(it) == 0:
                d[0].append(it[:it.find(':')])
                d[1].append(it[it.find(':') + 1:])
                if special_treatment.count(it) != 0:
                    d[2].append('[special treatment]')
                elif special_context.count(it) != 0:
                    d[2].append('[context specific]')
                else:
                    d[2].append('(not set/ignore)')
        e = sortListArray.sortListArray(d, 2)
        for i in range(0, len(b)): b[i].extend(e[i])
        ref_index = [], [], []
        for i in range(0, len(b[0])):
            # print structure
            # print b
            if type(b[2][i]) == list:
                if len(b[2][i]) > 2:
                    print b[2][i] + '\t' + level_refs[i] + '.\t' + b[0][i] + ':' + b[1][i]  # +'\t\t\t'+b[2][i]
            else:
                print b[2][i] + '\t\t\t' + level_refs[i] + '.\t' + b[0][i] + ':' + b[1][i]  # +'\t\t\t'+b[2][i]
            ref_index[0].append(level_refs[i])
            ref_index[1].append(b[0][i])
            ref_index[2].append(b[1][i])
            # ref_index[3].append(b[2][i])
    else:
        d = [], [], []
        for it in uniq_category:
            d[0].append(it[:it.find(':')])
            d[1].append(it[it.find(':') + 1:])
            if special_treatment.count(it) != 0:
                d[2].append('[special treatment]')
            elif special_context.count(it) != 0:
                d[2].append('[context specific]')
            else:
                d[2].append('(not set/ignore)')
        e = sortListArray.sortListArray(d, 0)
        ref_index = [], [], []
        for i in range(0, len(e[0])):
            if len(e[2][i]) > 2:
                print e[2][i] + '\t' + level_refs[i] + '.\t' + e[0][i] + ':' + e[1][i]
            else:
                print e[2][i] + '\t\t\t' + level_refs[i] + '.\t' + e[0][i] + ':' + e[1][i]
            ref_index[0].append(level_refs[i])
            ref_index[1].append(e[0][i])
            ref_index[2].append(e[1][i])
    print '---------------------------------------'
    return ref_index

def addSectionToData(data, structure):
    #--- add section information based on outline to data
    # data = type[0],page,color[2],text,charRange[4],section[5]
    data.append([])
    data.append([])
    for i in range(0, len(data[0])):
        data[5].append('')  # column for section
        data[6].append('')  # column for condition check
    special_treatment = getSpecialTreatment()
    stop = False
    # hold=[],[]
    count = 0
    for i in range(0, len(structure[0])):
        pt_type = structure[0][i]
        pt_color = structure[1][i]
        pt_section = structure[2][i]
        pt = 0
        for j in range(0, data[2].count(pt_color)):
            i_num = data[2].index(pt_color, pt)
            pt = i_num + 1
            count += 1
            if data[0][i_num] == pt_type and data[2][i_num] == pt_color:
                data[5][i_num] = pt_section
                # data[1][i_num] = pt_type
                data_type_color = str(data[0][i_num]) + ":" + str(data[2][i_num])
                if special_treatment.count(data_type_color) == 0:
                    data[5][i_num] = pt_section
    return data

# #changed "hold" to "data[0],[1]"

def fixIndents(data):
    last = 0
    for i in range(1, len(data[0])):
        try:
            if (eval(data[5][i - 1]) - eval(data[5][i])) * -1 >= 2:
                data[5][i] = str(eval(data[5][i - 1]) + 1)
                data[7][i] = ''
        except:
            data[5][i] = data[5][i - 2]
            data[7][i] = ''
            print 'ADDED BUT NOT PROPERLY OUTLINED: page', data[1][i], '(index= ' + str(i) + ')', data[3][i], '\n'       
    return data

def setOutline(data, structure, uniq_category, openFile):
    #--- get information on how to create outline based on notes
    # structure = type, color, section, format/style
    # print len(structure[0]),'  =  ',len(uniq_category)
    special_treatment = getSpecialTreatment()
    special_context = getSpecialContext()
    alphabet = 'abcdefghijklmnopqrstuvxyz'
    count = int(len(uniq_category) / len(alphabet)) + 1
    level_refs = []
    for i in range(1, count + 1):
        a = [i * j for j in alphabet]
        level_refs.extend(a)
    stop = False
    while stop == False:
        ref_index = customOutline(structure, uniq_category, level_refs)
        check = askQuestion('Do you want to change outline? (y/n)', "(y/n)?", ['y', 'n'])
        if check == 'y':
            step = askQuestion('What index do you want to change?',
                               "What index letter??",
                               level_refs)
            i_num = level_refs.index(step)
            structure_type_color = str(ref_index[1][i_num]) + ":" + str(ref_index[2][i_num])
            # print type(structure_type_color),structure_type_color
            # print
            if special_treatment.count(structure_type_color) != 0:
                checkSpecialTreatment(structure_type_color, 'check')
            elif special_context.count(structure_type_color) != 0:
                pass
                # checkSpecialTreatment(structure_type_color,'check')
            else:
                genericOutline()
                print '--- For', str(structure_type_color), " ---"
                outlineSection = askQuestion('What section of the outline?',
                                             "What number in the outline?",
                                             range(0, 6))
                # set_format = askQuestion('Do you want to add/change any formats? [Default is plain]','(y/n)',['y','n'])
                
                if len(structure[0]) == 0:
                    structure[0].append(ref_index[1][i_num])
                    structure[1].append(ref_index[2][i_num])
                    structure[2].append(str(outlineSection))
                    # if set_format == 'y': structure=setFormats(structure)
                    # else: structure[2].append('')
                else:
                    found = False
                    for i in range(0, len(structure[1])):  # range of colors
                        color = structure[1][i]
                        if color == ref_index[2][i_num]:
                            if structure[0][i] == ref_index[1][i_num]:                     
                                structure[2][i] = str(outlineSection)
                                # if set_format == 'y': structure=setFormats(structure,i)
                                found = True
                                break
                    if found == False:
                        structure[0].append(ref_index[1][i_num])
                        structure[1].append(ref_index[2][i_num])
                        structure[2].append(str(outlineSection))
                        # if set_format == 'y': structure=setFormats(structure)
        if check == 'n':
            stop = True
            break
        '''
        if structure[3] == 0:
            print ''
            print 'No formats are set for any outline level.'
        stopFormat = False
        while stopFormat == False:
            checkFormat = askQuestion('Do you want to change Format of any outline level? (y/n)',"(y/n)?",['y','n'])
            if checkFormat == 'y':
                step = askQuestion('What index do you want to change?',
                                   "What index letter??",
                                   level_refs)
                i_num=level_refs.index(step)
                structure_type_color=str(ref_index[1][i_num])+":"+str(ref_index[2][i_num])
                print '--- For', str(structure_type_color)," ---"
                if len(structure[0]) == 0:
                    print '\nMust make outline in order to apply Format.\n'
                    stopFormat=True
                    break
                structure=setFormats(structure,i_num)
            if checkFormat == 'n':
                stopFormat=True
                break
        '''
          
            
    # check = askQuestion('Do you want to change Format of any outline level? (y/n)',"(y/n)?",['y','n'])
    # if check == 'y':
    
    print len(data[0]), len(data[3])
    listFout.listFout(structure, 'var_' + str(openFile)[:-4] + "_structure.txt")
    listFout.listFout(data, 'var_' + str(openFile)[:-4] + "_data.txt")
    data = addSectionToData(data, structure)
    data = updateOutlineData(data, structure)
    data = setOutlineFormats(data)
    data = fixIndents(data)
    return data, structure
'''
    for m in range(0,len(uniq_category)):  #add styles
        if special_treatment.count(uniq_category[m]) != 0:
            checkSpecialTreatment(uniq_category[m],'check')
        else:
            genericOutline() 
            step = sectionQuestion(uniq_category[m])
            
            structure[0].append(uniq_category[m][:uniq_category[m].find(':')])
            structure[1].append(uniq_category[m][uniq_category[m].find(':')+1:])
            structure[2].append(str(step))

            genericStyles()
            steps = raw_input(":")
            x=str(level_refs).strip('[]').replace("'","").replace(',','').replace(' ','')
            y=len(step.strip(x).strip(','))
            while y == 0:
                print "What section of the outline?"
                print ''
                step = raw_input(":")
                x=str(level_refs).strip('[]').replace("'","").replace(',','').replace(' ','')
                y=step.strip(x).strip(',')
        #structure[3].append(x)
'''
 

def updateOutlineData(data, structure):
    # data = type[0],page,color[2],text,charRange[4],section[5]
    # structure = type, color, section, format/style
    # specialTreatments = conditions,criteria[...],note
        # criteria = type_colors,texts
    x = getConditions()  # conditions,values
    _criteria, _values, _notes = [y[0] for y in x], [y[1] for y in x], [y[2] for y in x]

    a, b, c = [], [], []
    for i in range(0, len(_criteria)):
        if type(_criteria[i]) == list:
            for j in range(0, len(_criteria[i])):
                a.append(_criteria[i][j])
                b.append(_values[i][j])
                c.append(i)
        else:
            a.append(_criteria[i])
            b.append(_criteria[i])
            c.append(i)
    conditions = [a, b, c]
  
    while data[6].count('') != 0:
        i = data[6].index('')
        data_type_color, data_text = str(data[0][i]) + ":" + str(data[2][i]), data[3][i]
        condition_met = False
        if conditions[1].count(data_type_color) != 0:
            pt = 0
            for j in range(0, conditions[1].count(data_type_color)):
                j_ind = conditions[1].index(data_type_color, pt)
                pt = j_ind + 1
                condition_num = conditions[2][j_ind]
                if conditions[2].count(condition_num) > 1:
                    if data_text.find(conditions[1][j_ind + 1]) != -1: condition_met = True
                    else: condition_met = False
                else: condition_met = True
                if condition_met == True: break
            if condition_met == True:
                data = actOnCondition(data, i, condition_num, structure)
            else: data[6][i] = 'updated'
        else: data[6][i] = 'updated'
    return data
      
def actOnCondition(data, i, condition_num, structure):
    x = getConditions()
    condition = x[condition_num]
    data_type_color = str(data[0][i]) + ":" + str(data[2][i])
    data[6][i] = 'updated'
    data, i = checkSubConditions(data, i, condition_num, structure)
    if condition[1][0] == 'k.highlight_note:orange':
        prevText, nextText = closestNote(data, i)
        data[3][i] = "<B>" + data[3][i].strip(' ') + "</B> = "
        if prevText < nextText:  # meaning: closest underlined text is BEFORE this underline
            data[3][i - 1] = data[3][i] + data[3][i - 1].lstrip(' ')
        else:
            data[3][i + 1] = data[3][i] + data[3][i + 1].lstrip(' ')
        for j in range(0, len(data)):
            x = data[j].pop(i)
    if condition[1][0] == 'k.underline_note:dark_green':
        data[3][i - 1] = data[3][i - 1].rstrip(' ') + ' ' + data[3][i].lstrip(' ')
        for j in range(0, len(data)):
            x = data[j].pop(i)
        data[6][i - 1] = 'updated'

    if condition[1][0] == 'k.underline_note:grey':
        prevText, nextText = closestNote(data, i)
        if prevText < nextText:  # meaning: closest underlined text is BEFORE this underline
            data[3][i - 1] = data[3][i].strip(' ') + ': ' + data[3][i - 1].lstrip(' ')
        else:
            data[3][i + 1] = data[3][i].strip(' ') + ': ' + data[3][i + 1].lstrip(' ')
        for j in range(0, len(data)):
            x = data[j].pop(i)
    if condition[1][0] == 'k.underline_note:light_blue':
        prev_color, prev_section = data[2][i - 1], data[5][i - 1]
        if prev_color == condition[1][0][condition[1][0].find(':') + 1:]:
            data[5][i] = data[5][i - 1]
        else:
            # print i
            # print prev_color,prev_section
            # print data[5][i]
            try:
                data[5][i] = str(eval(data[5][i - 1]) + 1)
            except:
                print i
                print ('Please check the outline for the black underline before page',
                       str(data[1][i]) + './n' + 'Be sure it includes the " v. " in the text of the black underline.')
                data[5][i] = str(eval(data[5][i - 2]) + 1)
    
    return data

def checkSubConditions(data, i, condition_num, structure):
    x = getConditions()
    condition = x[condition_num]
    data_type_color = str(data[0][i]) + ":" + str(data[2][i])
    if len(condition[0]) > 1:
        print ''
        if ((condition[0][0] == 'type_colors' and
            condition[1][0] == data_type_color)):
            if (condition[0][1] == 'text' and
            data[3][i].find(condition[1][1]) != -1):
                structure_type_colors = []
                for j in range(0, len(structure[0])):
                    structure_type_colors.append(structure[0][j] + ':' + structure[1][j])
                this_data_color = data[0][i] + ':' + data[2][i]
                this_section = data[5][i]
                above_outline_type_colors = structure_type_colors[0:structure_type_colors.index(this_data_color) + 1]
                for j in range(1, len(data[0][i:])):
                    data_type_colors = data[0][i + j] + ':' + data[2][i + j]
                    if above_outline_type_colors.count(data_type_colors) != 0:
                        end = i + j - 1
                        break
                s, e = i, end
                if end != i:
                    newConditions = []
                    for j in range(0, len(x)):
                        if len(x[j][0]) > 2:
                            initial_condition = x[j][1][:2]
                            if initial_condition == condition[1][:2]:
                                newConditions.append([x[j][0][2:], x[j][1][2:]])
                    condition_type_colors = [c[1][0] for c in newConditions]
                    condition_texts = [c[1][1] for c in newConditions]
                    total_added = 0
                    a1 = data[5].count("")
                    print 'first index number:', i
                    print 'number of data points with same color/type', e - s - 1  # '1' for title row
                    check = ['k.underline_note:dark_green', 'k.highlight_note:orange',
                           'k.underline_note:grey', 'k.underline_note:light_blue']
                    checkNum = 0
                    for c in range(s, e):
                        check_data_color = data[0][c] + ':' + data[2][c]
                        if check.count(check_data_color): checkNum += 1
                    print 'number of other_conditions', checkNum
                    print 'number of data points to change', e - s - checkNum - 1  # '1' for title row
                    a2 = 0
                    a3 = 0
                    total_added = 0
                    for it in condition_type_colors:  # for all conditions
                        _color = it[it.find(':') + 1:]
                        _type = it[:it.find(':')]
                        it_num = condition_type_colors.index(it)
                        _text = condition_texts[it_num]
                        # print _color,_type,_text
                        editRange = []
                        pt = 0
                        if data[2][s:e + 1].count(_color) != 0:
                            for k in range(0, data[2][s:e + 1].count(_color)):  # for data w/ color/type condition...
                                k_num = data[2][s:e + 1].index(_color, pt)
                                pt = k_num + 1
                                if data[0][k_num + s] == _type:
                                    editRange.append(k_num)
                        full_group, group, single = [], [], []
                        a2 += len(editRange)
                        last = False
                        while len(editRange) != 0:
                            if len(editRange) == 1:
                                if last == True: group.append(editRange.pop(0))
                                else: full_group.append(editRange.pop(0))
                            if len(editRange) == 0: break
                            a = editRange[0]
                            b = editRange[1]
                            if b - a == 1:
                                group.append(editRange.pop(0))
                                last = True
                            else:
                                if last == True:
                                    group.append(editRange.pop(0))
                                    full_group.append(group)
                                    group = []
                                else: full_group.append(editRange.pop(0))
                                last = False
                        
                        print _color, full_group
                        print ''
                        added = 0
                        if full_group != []:
                            for k in range(0, len(full_group)):
                                if type(full_group[k]) == list:
                                    # print 'group',full_group[k]
                                    group = full_group[k]
                                    for r in range(0, len(group)):
                                        data[5][group[r] + s] = str(eval(this_section) + 2)
                                    newDataPt = [data[0][group[0] + s],
                                                data[1][group[0] + s],
                                                data[2][group[0] + s],
                                                _text + ': ',
                                                data[4][group[0] + s],
                                                str(eval(this_section) + 1),
                                                'updated']                   
                                    for r in range(0, len(newDataPt)):
                                        data[r].insert(group[0] + s, newDataPt[r])
                                    added += 1
                                    e += 1
                                else:
                                    # print 'single',str(full_group[k]+s+added),data[3][full_group[k]+s+added]
                                    
                                    data[3][full_group[k] + s + added] = _text + ': ' + data[3][full_group[k] + s + added].lstrip(' ')
                                    data[5][full_group[k] + s + added] = str(eval(this_section) + 1)
                                    data[6][full_group[k] + s + added] = 'updated'
                        total_added += added
                    i = i + total_added
                    # print '2: ',data[5].count("")
                    print 'editRange:', a2
                    print 'data points added', e - end
                    
                    print 'remaining "" points.', data[5][s:e].count("")
                    print 'end index number', e
                    print '--------------------'
                    for k in range(s, e + 1):
                        print data[5][k], data[2][k], data[3][k]
                    print '--------------------'
                    print data[3][e]
                    print ""
    return data, i
    

def pickPageRange(a):
    print ''
    print 'In the PDF, there are notes between pages', a[0], 'and', a[len(a) - 1]
    page_range = range(a[0], a[len(a) - 1])
    start = askQuestion('What page do you want to start on?',
                                   "What page number letter??",
                                   page_range)
    print ''
    end = askQuestion('What page do you want to end on?',
                                   "What page number letter??",
                                   page_range)
    start, end = eval(str(start)), eval(str(end))
    if a.count(start) == 0:
        for i in range(0, start):
            i_num = start - i
            if a.count(i_num) != 0:
                start = a.index(i_num)
                break
    else:
        start = a.index(start)
    if a.count(end) == 0:
        for i in range(end, len(a)):
            if a.count(i) != 0:
                a.reverse()
                end = len(a) - a.index(i)
                break
    else:
        a.reverse()
        end = len(a) - a.index(end)
    start, end = eval(str(start)), eval(str(end))
    return start, end

def setFormats(structure, i= -1):
    formats = getWordFormats()
    formats.append('...FINISHED')
    options = []
    step = 'y'
    while step == 'y':
        if step == 'y':
            x = multiQuestion('Set/Add format:', formats)
            if x == formats.index('size'):
                var = askQuestion('Size of font?', 'What number size?', range(6, 72))
                x = [x, var]
            if x == '...FINISHED': step = 'n'  
            else: options.append(x) 
        print "\nFormats:"
        for it in options:
            print '-' + formats[eval(str(it)) - 1]
        print '\n---------------------\n'
        step = askQuestion('Add/change any more formats? (y/n)', '(y/n)', ['y', 'n'])
    if i == -1: structure[3].append(options)
    else:
        # print i
        # print len(structure[0])
        if len(structure[0]) != len(structure[3]):
            for j in range(0, len(structure[0]) - len(structure[3])):
                structure[3].append('(not set)')
        # print len(structure[3])
        structure[3][i] = options
    return structure

def setOutlineFormats(data):
    formats = [
        ['1', '2', '3', '4'],
         [
             ['bold', 'underline', 'caps', ['size', '16']],
             ['underline', 'caps', ['size', '14']],
             ['caps'],
             ['bold', 'underline']
         ]
        ]
    data.append([])
    for i in range(0, len(data[0])):
        data[7].append('')
        if formats[0].count(data[5][i]) != 0:
            f_num = formats[0].index(data[5][i])
            data[7][i] = formats[1][f_num]
    return data   
        

def checkFormat(data, i, structure):
    x = data[3][i]
    format_vars = [['<B>', '</B>'], 'IMPORTANT', 'BOLD', 'ITALIC', ['<I>', '</I>'],
                   'UNDERLINE', ['<U>', '</U>'], 'SIZE', 'CAPS']
    format = []
    for it in format_vars:
        if type(it) == list:
            for j in range(0, x.count(it[0])):
                p1, p2 = x.find(it[0]), x.find(it[1])
                find_txt, repl_txt = x[p1:p2 + 4], x[p1 + 3:p2]
                if p1 != -1 and p2 != -1:
                    if format_vars.index(it) <= 2:
                        formatText(find_txt, repl_txt, 'bold')
                        x = x.replace(find_txt, repl_txt)
                    elif 2 < format_vars.index(it) <= 4:
                        formatText(find_txt, repl_txt, 'italic')
                        x = x.replace(find_txt, repl_txt)
                    elif format_vars.index(it) == 6:
                        formatText(find_txt, repl_txt, 'underline')
                        x = x.replace(find_txt, repl_txt)                
        elif type(it) == str:
            if x.find(it) != -1:
                for j in range(0, x.count(it)):
                    if it == 'IMPORTANT':
                        formatText(x, x, 'caps')
                        formatText(x, x.replace(it, ''), 'bold')
                        x = x.replace(it, '')
                    elif it == 'BOLD':
                        formatText(x, x.replace(it, ''), 'bold')
                        x = x.replace(it, '')
                    elif it == 'ITALIC':
                        formatText(x, x.replace(it, ''), 'italic')
                        x = x.replace(it, '')
                    elif it == 'UNDERLINE':
                        formatText(x, x.replace(it, ''), 'italic')
                        x = x.replace(it, '')
                    elif it == 'SIZE':
                        s = x.find('SIZE')
                        pt = x[s + 4:s + 4 + 2]
                        formatText(x, x.replace(it + pt, ''), 'size', pt)
                        x = x.replace(it + pt, '')
                    elif it == 'CAPS':
                        formatText(x, x.replace(it, ''), 'caps')
                        x = x.replace(it, '')

    if data[7][i] != '':  # structure[0].count(data[5][i]) != 0 and structure[1].count(data[2][i]) != 0:
        # WordCmd('selectaboveparagraph')
        for format in data[7][i]:
            selectedText(format)
        # format=''
        # stop=False
        # for j in range(0,len(structure[0])):
        #    structure_type_data = structure[0][j]+':'+structure[1][j]
        #    this_type_data = data[0][i]+':'+data[2][i]            
        #    if this_type_data == structure_type_data:
        #        format=structure[3][j]
        #        break
        # WordCmd('selectaboveparagraph')
        # selectedText(format)
        WordCmd('selectbelowparagraph')

    return data

def CreateWordOutline(samplePath, page_range, structure, data, openFile):
    start, end = page_range
    offset = structure[4]
    a = date.today()
    today = a.strftime('%Y.%m.%d')
    title = today + '  --  ' + openFile
    copy(title)
    openWordFile(samplePath)
    WordCmd('paste')
    WordCmd('delete')
    first = True
    first = False
    for i in range(start, end):
        if data[5][i] != '':
            if data[5][i] != '1' and first == True:
                WordCmd('type', ' ')
                WordCmd('return')
            first = False
            clearFormats()
            WordCmd('type', '"')
            WordCmd('type', data[3][i])
            WordCmd('type', '" [' + str(eval(str(data[1][i])) + offset) + '] ')
            WordCmd('selectaboveparagraph')
            data = checkFormat(data, i, structure)
            top_slider, bottom_slider = Word_getIndent()  # inch = 72.0
            top = int(round(top_slider / 36, 1))
            bottom = int(round(bottom_slider / 36, 1))
            if eval(data[5][i]) == bottom:
                pass
            elif eval(data[5][i]) > bottom:
                # print 'right'
                for i in range(0, (eval(data[5][i]) - int(bottom))):
                    WordCmd('rightindent')
            elif eval(data[5][i]) < bottom:
                # print 'left'
                for i in range(0, (int(bottom) - eval(data[5][i]))):
                    WordCmd('leftindent')
            WordCmd('end')
            WordCmd('return')
            selectedText('(plain)')
        else:
            data_type_color = str(data[0][i]) + ":" + str(data[2][i])
            var = data, i
            checkSpecialTreatment(data_type_color, var)

    return 'Outline complete!'

def setOffset(pageCount, openFile):
    print ''
    print '-- You must setup the page number of the real document versus the PDF document. --'
    halfCount = int(round(pageCount / 2, 1))
    app(u'Skim').documents[openFile].go(to=app.documents[openFile].pages[halfCount])
    stop = 'n'
    while stop == 'n':
        PDF_page = askQuestion('Currently what page is the PDF?',
                                "Page number of the PDF?",
                                range(1, halfCount))
        Doc_page = askQuestion('Currently what page is the document?',
                                "Page number of the document?",
                                range(1, halfCount))
        x = str('Is the PDF on page ' + str(PDF_page) + ' while the document is on page ' + str(Doc_page) + '?  (y/n)?')
        stop = askQuestion(x, '(y/n)?', ['y', 'n'])
    offset = eval(str(Doc_page)) - eval(str(PDF_page))
    return offset

def makeSkimOutline():
    # data = type[0],page,color[2],text,charRange[4],section[5]
    # openFile, offset
    data = [[], [], [], [], []]

    # skim_colors,skim_types = skimVars()

    app(u'Skim').activate()
    app(u'Skim').windows[1].document.get()
    openFile = app(u'Skim').windows[1].document.name.get()
    print 'FILENAME: ', openFile, '\n'
    
    docPages = app(u'Skim').documents[openFile].get_pages_for()
    pageCount = len(docPages)

    # -- get note data
    data, uniq_category, uniq_page, skim_colors = getNotesFromSkim(data, openFile)

    #--- re-order notes according to page and characters           
    data = reOrderNotes(data, uniq_page)
    
    listFout.listFout(uniq_category, 'var_' + str(openFile)[:-4] + '_uniq_category.txt')
    listFout.listFout(data, 'var_' + str(openFile)[:-4] + '_data.txt')

    #--- get information on how to create outline based on notes
    #--- add section information based on outline to data
    #--- update data based on conditions

    try:
        structure = listFin.listFin('var_' + str(openFile)[:-4] + "_structure.txt")
    except:
        print ''
        print '-- You must setup the outline. --'
        offset = setOffset(pageCount, openFile)
        structure = [], [], [], [], offset
    
    data, structure = setOutline(data, structure, uniq_category, openFile)

    #--- add data to WORD OUTLINE

    # # WORD OUTLINE

    samplePath = 'MacOSX:Users:sethchase:Dropbox:Scripts:appscript:word_sample_outline.docx'
    offset = structure[4]

    a = list(data[1])
    start, end = pickPageRange(a)
    page_range = start, end
    # page_range=0,5

    status = CreateWordOutline(samplePath, page_range, structure, data, openFile)

    print '\r' + status

    return samplePath, page_range, structure, data, openFile



# samplePath,page_range,structure,data,openFile=makeSkimOutline()

######
# TEST --------------------
######
# '''
data = [[], [], [], [], []]

# skim_colors,skim_types = skimVars()

app(u'Skim').activate()
app(u'Skim').windows[1].document.get()
openFile = app(u'Skim').windows[1].document.name.get()
print 'FILENAME: ', openFile, '\n'
'''
docPages = app(u'Skim').documents[openFile].get_pages_for()
pageCount = len(docPages)

#-- get note data
data,uniq_category,uniq_page,skim_colors = getNotesFromSkim(data,openFile)

#--- re-order notes according to page and characters           
data = reOrderNotes(data,uniq_page)

listFout.listFout(uniq_category,'var_'+str(openFile)[:-4]+'_uniq_category.txt')
listFout.listFout(data,'var_'+str(openFile)[:-4]+'_data.txt')

#--- get information on how to create outline based on notes
#--- add section information based on outline to data
#--- update data based on conditions

try:
    structure = listFin.listFin('var_'+str(openFile)[:-4]+"_structure.txt")
except:
    print ''
    print '-- You must setup the outline. --'
    offset = setOffset(pageCount,openFile)
    structure = [],[],[],[],offset

data,structure = setOutline(data,structure,uniq_category,openFile)

#data = addSectionToData(data,structure)
#data = updateOutlineData(data, structure)
#data = setOutlineFormats(data)
#data = fixIndents(data)

"""
#--- add data to WORD OUTLINE

## WORD OUTLINE

samplePath = 'MacOSX:Users:sethchase:Dropbox:Scripts:appscript:word_sample_outline.docx'
offset=structure[4]

#a=list(data[1])
#start,end=pickPageRange(a)
#page_range = start,end
page_range=145,len(data[0])

status = CreateWordOutline(samplePath,page_range,structure,data,openFile)
#trouble at i=50

print '\r'+status
"""
'''
######
# TEST --------------------
######
# """
data = listFin.listFin('var_' + str(openFile)[:-4] + '_data.txt')
structure = listFin.listFin('var_' + str(openFile)[:-4] + '_structure.txt')
uniq_category = listFin.listFin('var_' + str(openFile)[:-4] + '_uniq_category.txt')

print len(data[0]), len(data[3])
data = addSectionToData(data, structure)
print len(data[0]), len(data[3])
print 'missing points', data[5].count("")
data = updateOutlineData(data, structure)
data = setOutlineFormats(data)
data = fixIndents(data)

# """
"""
for j in range(0,len(data[0])):
    string=''
    try:
        for k in range(0,eval(data[5][j])):
            string+='\t'
    except:
        pass
    print j,string+'XXXX'#string+data[5][j],data[2][j],data[3][j]
"""

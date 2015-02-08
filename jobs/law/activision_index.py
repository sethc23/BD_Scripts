from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts')
path.append('/Users/admin/SERVER2/BD_Scripts/html')
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from writeHTML import makeHTML, addTag, makeTableFromList, tableRow
from writeHTML import makeTableFromRows, hyperlink, horizontalRule
import os
from files_system_commands import getAllFilePaths
from datetime import datetime
from AS_Skim import openPDF, setSkimWindowLeft, closePDF
from sortListArray import sortListArray


def checkPDFS(workDir, files):
    undated = []
    if len(files) != 0:
        for it in files:
            indexNum = noDate.index(it)
            openPDF(workDir + it)
            setSkimWindowLeft()
            dateInput = raw_input("Date of Document? (n = none)\n")
            print ''
            if dateInput == 'n':
                undated.append(noDate[indexNum])
                closePDF(it[it.rfind('/') + 1:])
            else:
                oldPath = workDir + it
                oldPath = oldPath.replace(' ', '\ ')
                newPath = workDir + it.replace(' ', '_')
                newPath = newPath.replace('.PDF', '.pdf')
                newPath = newPath.replace('.pdf', ' ' + dateInput + '.pdf')
                newPath = newPath.replace(' ', '\ ')
                cmd = 'mv ' + oldPath + ' ' + newPath
                os.system(cmd)
                closePDF(it[it.rfind('/') + 1:])
    return undated


workDir = '/Users/admin/Desktop/Activision/all_boxes'
# #292 files
getContents = os.listdir
checkFolder = os.path.isdir

files = getAllFilePaths(workDir)

indexNum = files.index('/Users/admin/Desktop/Activision/all_boxes/activision.html')
files.pop(indexNum)


checkedFiles = [
'/01-07-85_to_04-16-85/Exhibit_A.pdf',
'/01-07-85_to_04-16-85/Settlement_Agreement.pdf',
'/02-04-83_to_02-28-83/Plaintiffs_Response_To_Defendants_First_Set_Of_Interrogatories_nos._1-125_copy.pdf',
'/02-22-86_to_06-27-86/Proposed_Amended_Judgment.pdf',
'/01-07-85_to_04-16-85/Plaintiffs_Pretrial_Proposed_Conclusion_Of_Law.pdf',
'/02-28-83_to_05-27-83/Formal_Opinions_Nos._176-177.pdf',
'/02-04-83_to_02-28-83/Plaintiffs_Response_To_Defendants_First_Set_Of_Interrogatories_nos._1-125.pdf',
'/06-20-83_to_08-19-83/Proposed_Order_Compelling_Plaintiffs_To_Provide_Further_Answers.pdf',
'/07-10-84_to_08-30-84/Memorandum_Of_Points_And_Authorities_In_Support_Of_Defendant_Motion_For_Order.pdf',
'/07-10-84_to_08-30-84/Plaintiffs_Third_Supplemental_Response_To_Defendants_Interrogatories_2.pdf',
'/09-01-82_to_12-20-82/Affidavit_Of_Thomas_Briody.pdf',
'/09-01-82_to_12-20-82/Complaint_For_Patent_Infringement.pdf',
'/09-01-82_to_12-20-82/Plantiffs_Proposed_Form_Of_Order_To_Dismiss_First_And_Third_Counterclaims.pdf',
'/09-01-82_to_12-20-82/Reply_To_First_And_Third_Counterclaims.pdf',
'/09-12-84_to_12-06-84/Plaintiffs_Exhibits_For_Their_Prima_Facie_Case_C825270Jpv.pdf',
'/09-12-84_to_12-06-84/Plaintiffs_Proposed_Points_Of_Law_C825270Jpv.pdf',
'/12-29-82_to_02-04-83/Declaration_Of_Scott_Hover-Smoot.pdf',
'/12-29-82_to_02-04-83/Preservation_Of_Competition_16600.pdf',
'/12-29-82_to_02-04-83/Surreply_Memorandum_In_Support_Of_Plaintiff_Motion_To_Dismiss_2Nd_Counterclaim.pdf',
'/Go_to_Games_Folder/Simax.pdf',
'/Miscellaneous_Papers/Activision_Games.pdf',
'/06-20-83_to_08-19-83/Idi_Pool_Demonstration 10Jul84.pdf',
'/08-31-84_to_09-10-84/Exhibit_A-A.pdf',
'/08-31-84_to_09-10-84/Exhibit_B-B.pdf',
'/08-31-84_to_09-10-84/Exhibit_B.pdf',
'/08-31-84_to_09-10-84/Exhibit_C.pdf',
'/08-31-84_to_09-10-84/Exhibit_D.pdf',
'/08-31-84_to_09-10-84/Exhibit_E.pdf',
'/08-31-84_to_09-10-84/Exhibit_F.pdf',
'/08-31-84_to_09-10-84/Exhibit_G.pdf',
'/02-22-86_to_06-27-86/Declaration_Of_Marla_J_Miller_In_Support_Of_Acts_Brief_Re_Magnavox_Motion_To_Dismiss_Appeal.pdf',
'/02-28-83_to_05-27-83/Reply_To_Second_Counterclaim_2.pdf',
'/06-20-83_to_08-19-83/Plaintiffs_Response_To_Defendants_Second_Set_Of_Interrogatories_nos_126-182_copy.pdf',
'/06-20-83_to_08-19-83/Shipping_Records.pdf',
'/07-10-84_to_08-30-84/Plaintiffs_Third_Supplemental_Response_To_Defendants_Interrogatories.pdf',
'/09-01-82_to_12-20-82/Affidavit_Of_Robert_T_Mayer.pdf',
'/09-01-82_to_12-20-82/Notice_Of_Motion_And_Plaintiffs_Motion_To_Dismiss_Second_Counterclaim.pdf',
'/09-01-82_to_12-20-82/Plantiffs_Proposed_Form_Of_Order_To_Dismiss_Second_Counterclaims.pdf',
'/09-01-82_to_12-20-82/Reply_To_First_And_Third_Counterclaims_2.pdf',
'/09-12-84_to_12-06-84/Plaintiffs_Pretrial_Statement_Response_C826270Jpv.pdf',
'/09-12-84_to_12-06-84/Plaintiffs_Statement_Of_Factual_Issues_C825270Jpv.pdf',
'/12-29-82_to_02-04-83/Joint_Certificate_Of_Counsel.pdf',
'/12-29-82_to_02-04-83/Sanders_Response_To_Activision_Interrogatories.pdf',
'/Binders/Briody-Levy_Activision_1985.pdf',
'/Go_to_Games_Folder/Wsj_-_Article_Video_Games_Revive.pdf'
    ]

'''
checkedFiles=[]
x=0
for it in files:
    z=it.split(' ')
    a=z[len(z)-1].replace('.pdf','').replace('.PDF','').replace('-','')
    try:
        b=datetime.strptime(a,'%d%b%y')
        htmlDate=b.strftime('%d-%B %Y')
        sortableDate=b.strftime('%Y.%m.%d')
    except:
        if checkedFiles.count(it) != 0:
            pass
        else:
            x=x+1
            print it
print x
'''
'''
x=0
noDate,ignored=[],[]
for it in files:
    if checkedFiles.count(it) != 0:
        pass
    else:
        z=it.split('_')
        a=z[len(z)-1].replace('.pdf','').replace('.PDF','').replace('-','')
        try:
            b=datetime.strptime(a,'%d%b%y')
            htmlDate=b.strftime('%d-%B %Y')
            sortableDate=b.strftime('%Y.%m.%d')
        except:
            print it
            print ''
            move=raw_input("(1) Change filename \n(2) Open in Acrobat\n(3) Ignore \n(4) Quit\n")
            print ''
            if move == '1':
                print ''
                filePath = raw_input("type new file path:\n")
                print ''
                oldPath=workDir+it
                oldPath=oldPath.replace(' ','\ ')
                newPath=workDir+filePath
                newPath=newPath.replace(' ','\ ')
                cmd = 'mv '+oldPath+' '+newPath
                os.system(cmd)
            elif move == '2':
                noDate.append(it)
            elif move == '3':
                ignored.append(it)
            elif move == '4':
                break     
            else:
                break

            #show variable, ask to change or open in acrobat
            #if open in acrobat, add to list and keep going

undated = checkPDFS(workDir,noDate)
print ''
print 'undated/ignored'
print ''
if len(undated) != 0:
    for it in undated:
        print "'"+it+"',"
if len(ignored) != 0:
    for it in ignored:
        print "'"+it+"',"

'''
'''
words=[]
for it in files:
    z=it[it.rfind('/')+1:-4]
    z=z.split(' ')
    for pt in z:
        if words.count(pt) == 0:
            words.append(pt)


saveFile='/Users/admin/Desktop/wordList.txt'
f=open(saveFile,'w')
for it in words:
    text="('"+it+"':'')"+'\n'
    f.writelines(text)
f.close()
'''
# get dictionary, split into old/new lists
'''
saveFile='/Users/admin/Desktop/wordList.txt'
f=open(saveFile,'r')
x=f.read()
f.close()
x=x.replace('\n','\r')
x=x.split('\r')

oldWords,newWords,checkWords=[],[],[]
for pt in x:
    pt=pt.lower()
    old,new=pt.split(':')[0][2:-1],pt.split(':')[1][1:-2]
    old=old.lower()
    new=new.lower()
    oldWords.append(old)
    newWords.append(new)
    #if new == '':
        #checkWords.append(old)
'''
# make dictionary for corrections to file names
'''
fixedWords=[]
for it in files:
    z=it[it.rfind('/')+1:-4]
    z=z.split(' ')
    for pt in z:
        if checkWords.count(pt) != 0:
            if fixedWords.count(pt) == 0:
                openPDF(workDir+it)
                setSkimWindowLeft()
                print it
                print ''
                txt=raw_input(pt+"  -- change too...\n")
                fixedWords.append(txt)
                closePDF(it[it.rfind('/')+1:])
'''
# change file names based off dictionary
'''
for it in files:
    z=it[it.rfind('/')+1:-4]
    z=z.split(' ')
    newText=''
    for pt in z:
        if oldWords.count(pt.lower()) != 0:
            indexNum=oldWords.index(pt.lower())
            newText=newText+newWords[indexNum].title()+' '
        else:
            newText=newText+pt.title()+' '
    newText=newText.rstrip()
    newText=newText+'.pdf'
    newPath=it[:it.rfind('/')+1]+newText
    newPath=newPath.replace(' ','_')

    oldPath=it.replace(' ','\ ')
    newPath=newPath.replace(' ','\ ')
    oldPath=workDir+oldPath
    newPath=workDir+newPath
    cmd = 'mv '+oldPath+' '+newPath
    #print cmd
    os.system(cmd)
    #print cmd
    #break
'''
# make filename word substitutions from file 
'''
replFile='/Users/admin/Desktop/replacements.txt'
f=open(replFile,'r')
x=f.read()
f.close()

oldWords,newWords=[],[]
x=x.split('\n')
for it in x:
    oldWords.append(it.split('\t')[0])
    newWords.append(it.split('\t')[1])
    

for it in files:
    z=it.split('_')
    edit=False
    text=''
    for pt in z:
        if oldWords.count(pt) != 0:
            indexNum=oldWords.index(pt)
            text=text+newWords[indexNum]+'_'
            edit=True
        else:
            text=text+pt+'_'
    text=text.rstrip('_')
    if edit == True:
        oldPath=it
        newPath=text
        oldPath=workDir+oldPath
        newPath=workDir+newPath
        cmd = 'mv '+oldPath+' '+newPath
        #print cmd
        os.system(cmd)
        #print cmd
        #break
x'''    

# #links broken up by year
# #header row {date,document}
# #column for date
# makeHTML, addTag, makeTableFromList,tableRow
# '''
headerRow = []
headerRow.append(addTag('b', 'Date'))
headerRow.append(addTag('b', 'Title'))

tableRows = []
tableRows.append(tableRow(headerRow, ['120', '480']))

# sort content
fileNames, fileDates = [], []
for it in files:
    z = it.split('_')
    a = z[len(z) - 1].replace('.pdf', '').replace('.PDF', '').replace('-', '')
    name = it[it.rfind('/') + 1:].replace('.pdf', '').replace('.PDF', '').replace('_', ' ')
    try:
        b = datetime.strptime(a, '%d%b%y')
        htmlDate = b.strftime('%d-%B %Y')
        sortableDate = b.strftime('%Y.%m.%d')
        fileDates.append(str(sortableDate))
        name = name.replace(a, '')
        fileNames.append(name)
    except:
        fileNames.append(name)
        if it.find('_to_') != -1:
            folder = it[it.find('_to_') + 4:it.find('/', 1)]
        else:
            folder = it[1:it.find('/', 1)]
        if folder.find('-') != -1:
            b = datetime.strptime(folder, '%m-%d-%y')
            sortableDate = b.strftime('%Y.%m.%d')
            fileDates.append(str(sortableDate) + '-')     
        else:
            fileDates.append('----')
            print folder
            # print it
            
print len(files), ' = ', len(fileDates), ' = ', len(fileNames)

fileLinks = []
for i in range(0, len(files)):
    fileLinks.append(hyperlink(fileNames[i], files[i][1:]))

newList = (fileDates, fileLinks)

sortedList = sortListArray(newList, 0)


for i in range(0, len(sortedList[0])):
    date, link = sortedList[0][i], sortedList[1][i]
    if date.find('-') != -1:
        date = '----'
    else:
        b = datetime.strptime(date, '%Y.%m.%d')
        date = b.strftime('%d-%b-%Y')
    tableRows.append(tableRow([date, link]))


htmlTable = makeTableFromRows(tableRows, '600') 
html = makeHTML(htmlTable, 'Magnavox v Activision Litigation')
htmlFile = '/Users/admin/Desktop/Activision/all_boxes/activision.html'

f = open(htmlFile, 'w')
f.write(html)
f.close()
# '''


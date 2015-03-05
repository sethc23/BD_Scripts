from os import getcwd as os_getcwd
#import subprocess
from sys import argv, path
from bs4 import BeautifulSoup
from urllib import quote_plus#,unquote
# from re import match
# from htmlentitydefs import name2codepoint
from os import environ as os_environ
from os import path as os_path
from sys import path as py_path
py_path.append(os_path.join(os_environ['BD'],'html/xgoogle'))
#from IPython import embed_kernel as embed
#embed()
from search import GoogleSearch

def getSoup(x):
    if type(x) == str: return BeautifulSoup(x)
    if type(x) == unicode: return BeautifulSoup(x)
    else: return BeautifulSoup(x.contents[0])

def FindAllTags(text,tag):
    a=getSoup(text)
    return a.findAll(tag)

def getAllTag(text, tag):
    h = BeautifulSoup(text)
    get_tags=['href','img']
    if get_tags.count(tag) != 0:
        x = h('a')
        a = []
        for it in x:
            a.append(it.get(tag))
    else:
        x = h(tag)
        a = []
        for it in x:
            s, l = '', it.contents
            for pt in l: s += str(pt)
            a.append(s)
    return a

def getInnerElement(text, tag, tag_var):
    soup = BeautifulSoup(text)
#     get_tags=['a','img']
#     if get_tags.count(tag) != 0:
    s='result = soup.'+tag+"['"+tag_var+"']"
    try:
        exec s
    except:
        print s
        print text
        exec s
    return result

def getTagContents(text, tag, tag_var=""):
    soup = BeautifulSoup(text)
    if tag == 'class': return str(soup(tag, id='"' + tag_var + '"')[0].contents)   
    if tag_var == 'text': return soup(tag)[0].contents

def getTagsByAttr(text, tag, attr='',contents=True): # attr = { "class" : "sister" }
    soup = BeautifulSoup(text)
    if attr=='': a=soup.find_all(tag)
    else: a=soup.find_all(tag, attr)
    if contents==True:  return str(a[0].contents)
    if contents == False: return a

def getInnerHTML(html):
    return "".join([str(x) for x in html.contents]) 

def safe_url(url):
    return quote_plus(url)

class google:

    def __init__(self):
        self.gs = GoogleSearch('')
    
    def get_results(self,src):
        if src != '': 
            return self.gs._extract_results(BeautifulSoup(src))
        



def addTag(tag, text, option=''):
    if option != '': return '<' + tag + ' ' + option + '>' + text + '</' + tag + '>'
    else: return '<' + tag + '>' + text + '</' + tag + '>'

def horizontalRule():
    return '<hr />'

def html_space():
    return '&nbsp;'

def hyperlink(title, link, place='_blank'):
    text = '<a href="' + link + '"'
    text = text + ' target="' + place + '">'
    text = text + title + '</a>'
    return text

def readTable(table):
    soup = BeautifulSoup(table)
    rows=soup.findAll('tr')
    table=[]
    for j in rows:
        jrow=[]
        for i in j.findAll('td'):
            jrow.append(i.contents)
        table.append(jrow)
    print type(table),len(table[1]),table[1]
    return table
        

def tableRow(columnData, widths=False):
    row = ''
    for i in range(0, len(columnData)):
        it = columnData[i]
        text = addTag('td', it)
        if type(widths) != bool:
            if ((len(columnData) != len(widths))
                or (type(columnData) != type(widths))):
                print 'writeHTML.tableRow error'
                print len(columnData), ' != ', len(widths)
                print type(columnData), ' != ', type(widths)
                return 'error'
            else:
                text = text.replace('<td>', '<td width="' + widths[i] + '">')
        row = row + text + '\n'
    return row

def makeTableFromList(list_data, list_options, width="450", border="1", align="center"):
    # if type(list_data[0]) != list: list_data = [list_data]
    if list_options == '': list_options = [[''] for it in list_data]
    text = '<table width="' + width + '" border="' + border + '" align="' + align + '">\n'
    for i in range(0, len(list_data)):
        row = list_data[i]
        row_option = list_options[i]
        col_data = ''
        if type(row) == list:
            for j in range(0, len(row)):
                col = row[j]
                col_option = row_option[j]
                if col_option == '': pt = addTag('td', col) + '\n'
                else: pt = addTag('td', col, col_option) + '\n'
                col_data = col_data + pt
        else:
            col_data = addTag('td', row) + '\n'
        row_data = addTag('tr', col_data) + '\n'
        text = text + row_data
    text = text + '</table>\n'
    return text

def makeTableFromRows(list_data, width="200", border="1"):
    text = '<table width="' + width + '" border="' + border + '" cellpadding="0" cellspacing="0">'
    data = ''
    for row in list_data:
        data = addTag('tr', row)
        text += data + '\n'
    text = text + '</table>'
    return text

def makeTableFromTableRows(tableRows, width="100%", border="1"):
    text = '<table width="' + width + '" border="' + border + '" cellpadding="0" cellspacing="0">'
    text += tableRows
    return text + '</table>'

def makeListFromList(list_data):
    text = '<ul>'
    for it in list_data:
        data = '<li>' + it + '</li>\n'
        text = text + data
    text = text + '</ul>\n'
    return text

def makeHTML(text, title='Untitled Document'):
    header = ('''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n
    <html xmlns="http://www.w3.org/1999/xhtml">\n
    <head>\n
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n
    <title>#TITLE#</title>\n
    </head>\n
    ''')
    header = header.replace('#TITLE#', title)
    body = addTag('body', text)
    html = header + body + '\n' + '</html>'
    return html



def makeTableRowsFromFilePaths(workDir, fpaths, folderStyle='f_1', fileStyle='f_2'):
    rows, folders = [], []
    dbl_space = html_space() + html_space()
    for it in fpaths:
        # print it
        tempCol = ''
        html_folder = it.replace(workDir, '')  # LECTURES/*
        # print it
        # if it.find('/') != -1:
        pathSplit = html_folder.split('/')
        # note, return fpaths does not contain folder references, just file references
        pathSplit_lastItem = pathSplit[len(pathSplit) - 1]
        pathSplit_lastFolder = pathSplit[len(pathSplit) - 2]
        pathSplit_lastFolderPath = it[:it.rfind('/')].replace(workDir, '')
        # print pathSplit_lastFolderPath
        # print workDir
        # print sfdgf
        tempFolder, tempPath = '', ''
        indent = ''
        if folders.count(pathSplit_lastFolder) == 0:
            folders.append(pathSplit_lastFolder)
            if pathSplit_lastFolderPath != '':
                rows.append(addTag('td', pathSplit_lastFolderPath, 'class="' + folderStyle + '"'))
            # else: rows.append(addTag('td','/'+pathSplit_lastFolderPath,'class="'+folderStyle+'"'))
            # print pathSplit_lastFolder
            # print '"',indent+pathSplit_lastFolder,'"'
        indent = ''
        for j in range(0, len(pathSplit) - 1):
            for l in range(0, 6): indent += html_space()
        title = pathSplit_lastItem
        url = it.replace(workDir, '')
        link = hyperlink(title, 'contents/' + url.strip('/'))
        # print link
        # print dasa
        rows.append(addTag('td', indent + link, 'class="' + fileStyle + '"'))
        # print it
    return rows

def offsetPageNum(pgnum, fileLink):
    changeVars = [['3', 'PIPA_4th_OCR.pdf'], ['3', 'PIPA_5th_OCR.pdf'], ['3', 'PIPA_6th_OCR.pdf'], ['3', 'PIPA_7th_OCR.pdf'], ['3', 'PIPA_8th_OCR.pdf'], ['0', 'PIPA_9th_OCR.pdf'], ['3', 'PIPA_10th_OCR.pdf'], ['4', 'PIPA_11th_OCR.pdf'], ['5', 'PIPA_12th_OCR.pdf'], ['5', 'PIPA_13th_OCR.pdf'], ['5', 'PIPA_14th_OCR.pdf'], ['6', 'PIPA_15th_OCR.pdf'], ['6', 'PIPA_16th_OCR.pdf'], ['5', 'PIPA_17th_OCR.pdf'], ['4', 'PIPA_18th_OCR.pdf'], ['6', 'PIPA_19th_OCR.pdf'], ['5', 'PIPA_20th_OCR.pdf'], ['0', 'PIPA_21st_OCR.pdf'], ['4', 'PIPA_22nd_OCR.pdf']]
    offsets, filenames = [], []
    for it in changeVars:
        offsets.append(eval(it[0]))
        filenames.append(it[1])
    if filenames.count(fileLink) != 0:
        pg_offset = offsets[filenames.index(fileLink)]
        # print pgnum
        pgnum = eval(str(pgnum)) + eval(str(pg_offset))
        # print pgnum
        pgnum = hyperlink(str(pgnum), '../hosted_resources/PIPA_docs/' + fileLink + '#page=' + str(pgnum))
    return str(pgnum)

def scrap(workDir):
    newHtml = ''

    f = open('/Users/admin/Desktop/PIPA_user8.html', 'r')
    x = f.read()
    f.close()

    f = open('/Users/admin/Desktop/PIPA_Papers/index.html', 'r')
    y = f.read()
    f.close()
    w = getAllTag(y, 'td')
    w.pop(0)
    e = []
    for it in w:
        if it[27].isdigit() == False and it[24].isdigit() == True:
            e.append(getAllTag(it, 'href')[0])
    
    # def get
    a = getAllTag(x, 'tr')
    b = getAllTag(x, 'a')

    # get all headings and sub headings
    c = getAllTag(x, 'span')
    d, f = [], [[], []]
    pt = 0
    for it in c: 
        pt = x.find(it, pt)
        if it.find(':') != -1: 
            s = it.find(':')
            s1 = it[:s].rfind('>') + 1
            s2 = it.find('<', s) - 1
            d.append(it[s1:s2])  # d=headings
        else:
            f[0].append(pt)
            h1 = getAllTag(it, 'font')
            f[1].append(h1)
    for it in f[1]: 
        try:
            print it[0]
        except:
            print 'error', it
    
    linkTitles, pgNums, headings, spans, docTitles = [], [], [], [], []
    pt, oldNum = 0, 500
    html_pt, head_ind, head_pt, sub_heading, newSub = 0, 0, 0, '', ''
    tempTableData, linkFile = [], ''
    for i in range(0, len(a)):
        it = a[i]
        cols = getAllTag(it, 'td')
        pg = cols[1]
        try: 
            # print i,'-oldNum-"'+str(oldNum)+'"'
            if eval(str(pg)) >= eval(str(oldNum)): 
                oldNum = pg
                # print 'heading'
            else:
                newHtml += makeTableFromRows(tempTableData, "100%")
                tempTableData = []
                h = d[pt].replace('\n', '')  # d=headings
                print h
                h_url = '../hosted_resources/' + e[pt]
                linkFile = e[pt][e[pt].find('/') + 1:]
                newHtml += '<hr width="100%">'
                link_title = addTag('font', h, option='class="f_1"')
                link_title = addTag('span', link_title, option='class="b"')
                newHtml += hyperlink(link_title, h_url, place='_blank')
                pt += 1
                oldNum = 0

        except: 
            pass
        
        title = cols[0].replace('\n', '')
        
        html_pt = x.find(title, html_pt) + 1
        # print newSub
        # print head_pt
        # head_pt=x.find(newSub,head_pt)+1
        if newSub != sub_heading:
            sub_heading = newSub
            if sub_heading != '\n':
                print '\t', sub_heading
                if pgNums == [] and linkTitles == []: pass
                else:
                    newHtml += makeTableFromRows(tempTableData, "100%")
                    span_sub = addTag('font', sub_heading, option='class="f_2"')
                    span_sub = addTag('span', span_sub, option='class="b"')
                    newHtml += span_sub
                    tempTableData = []
                    # tempClear=True
        
        last_row_pt = len(a) - 1
        last_head_pt = len(f[1]) - 1
        if i == last_row_pt or head_ind == last_head_pt:
            newSub = f[1][last_head_pt][0]
        else:
            next_row_pt = x.find(a[i + 1], html_pt)
            # print '<--\n'
            # print 'next_row_pt,a[i+1]\t\t',next_row_pt,a[i+1].replace('\n','')
            next_head_pt = x.find(f[1][head_ind][0], html_pt)
            # print 'next_head_pt,f[1][head_ind][0]\t',next_head_pt,f[1][head_ind][0]
            next_main_head_pt = x.find(d[pt], html_pt)
            # print 'next_main_head_pt,d[pt]\t\t',next_main_head_pt,d[pt]
            # print '-->\n'
            if (next_row_pt - html_pt) < (next_head_pt - html_pt):  pass  # next point is a data row (not a heading)
            else:
                if (next_head_pt - html_pt) < (next_main_head_pt - html_pt):
                    if (next_row_pt - html_pt) < (next_main_head_pt - html_pt):
                        newSub = f[1][head_ind][0]
                        head_ind += 1

        pg = pg.replace('\n', '').replace('<p>', '').replace('</p>', '')
        if pg == 0: pg = ' '
        print '\t', '\t', pg, '\t', title
        if pg != '': 
            if pg.isdigit() == True: editPg = offsetPageNum(pg, linkFile)
        else: editPg = pg
        pg = editPg
        pgNums.append(pg)
        linkTitles.append(title)
        tempTableData.append(addTag('td', pg, 'class="td_1"') + addTag('td', title, 'class="td_2"'))

        headings.append(h)
        # if i == 5: break
        # spans.append(s)
    newHtml += makeTableFromRows(tempTableData, "100%")
    print 'len(pgNums),len(linkTitles),len(headings)=', len(pgNums), len(linkTitles), len(headings)

    f = open('/Users/admin/Desktop/PIPA_user8_template.html', 'r')
    html_template = f.read()
    f.close() 
    
    last_html = html_template.replace('#BODY#', newHtml)
    
    f = open('/Users/admin/Desktop/PIPA_user8_v2.html', 'w')
    x = f.write(last_html)
    f.close()   
'''
b=getAllTag(x,'table')
print b[0]

print len(b),len(c)    
heading,linkTitles,page=[],[],[]
for i in range(0,len(b)):
    s1=x.find(table)
    if i == len(b)-1: s2=len(x)
    else: s2=x.find(b[i+1]) # find begining of next table
    workSec=x[s1:s2]
    if workSect.find(c[i]):
'''
        
        
        
    

if __name__ == '__main__':
    try:
        cmd = []
        cmd.append(os_getcwd() + '/')
        for i in range(1, len(argv)): cmd.append(argv[i])
            # cmd[0] == current working directory
            # cmd[1] == function to apply
            # cmd[2] == variable for the function
        # print cmd
        stop = False
    except:
        cmd = []
        pass
        stop = True
    if cmd == []: pass
    else:
        # print len(cmd)
        if cmd[1] == 'scrap': scrap(cmd[0])  # #  in this directory replace {1} with {2}     {1}="{'a','b'}"
        
        
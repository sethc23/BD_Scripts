
from sys import argv, path
from bs4 import BeautifulSoup
# path.append('/Users/admin/SERVER2/BD_Scripts/utility')
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import getFilesFolders,pdfPageCount,click
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from HTML_API import getAllTag
from webpage_scrape import runLink
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from Chrome_API import activate, openUrl, runScript,checkLoaded


def compare_index_data(cases_on_file, files_checked):
    
    f = open(cases_on_file, 'r')
    onfile = f.readlines()
    f.close
    '''
    f=open('/Users/admin/Desktop/cases_on_file.txt','r')
    z=f.read()
    f.close
    print repr(z[:100])
    '''
    
    f = open(files_checked, 'r')
    checked = f.readlines()
    f.close
    
    a = "test"
    
    
    
    a = checked
    b = onfile
    
    print a[0].rstrip('\r\n')
    print b[0].rstrip('\r\n')
    
    ch_id, ch_name = [], []
    for it in a:
        x, y = it.split('<->')
        ch_id.append(x.lower())
        ch_name.append(y.lower().rstrip('\r\n'))
    
    last, first, full, f_id = [], [], [], []
    for it in b:
        x = it.split('<->')
        last.append(x[0].lower())
        first.append(x[1].lower())
        full.append(x[2].lower())
        f_id.append(x[3].lower().rstrip('\r\n'))
    
    c = []
    for it in ch_id:
        if c.count(it) == 0:
            c.append(it)
            print it
    
    print sdfgsd 
    
    print ch_id[0], ch_name[0]
    print f_id[0], full[0], last[0], first[0]
    print ''
    
    print "Cases on File where plaintiff was in index number searched"
    print ''
    print 'F-capt\tF-id\tCh-id\tCh-Capt'
    # print len(ch_id),len(last)
    new = []
    for i in range(0, len(ch_id)):
        comp_id = ch_id[i]
        if f_id.count(comp_id) != 0:
            file_index = f_id.index(comp_id)
            st_ch = ch_id.index(comp_id)
            for j in range(0, ch_id.count(comp_id)):
                if ch_name[st_ch + j].count(first[file_index]) != 0 and ch_name[st_ch + j].count(last[file_index]) != 0:
                    if new.count(full[file_index]) == 0:
                        new.append(full[file_index])
                        print full[file_index] + '\t' + f_id[file_index] + '\t' + ch_id[i + j] + '\t' + ch_name[i + j] + '<->'
def compare_text(x, folder1, folder2, test_var):
    for i in range(0, len(x)):
        # try:
        # if a[i] == '102149-2005': stop=False
        workfold1 = folder1 + a[i] + test_var
        workfold2 = folder2 + a[i] + test_var
        f = open(workfold1, 'r')
        x = f.read()
        f.close()        
        f = open(workfold2, 'r')
        y = f.read()
        f.close()       
        if len(x) != len(y):  
            print workcomp[workcomp.rfind('/'):]
            z += 1
        print 'number of non-matches', z

    

def scrape_pages(x, workfold):
    for i in range(0, len(x)):
        gotoUrl = 'http://iapps.courts.state.ny.us/iscroll/CaseCap.jsp?IndexNo=' + x[i]
        # print gotoUrl
        runLink(gotoUrl, x[i], workfold)

def scrape_elaw(x=""):
    for it in x[958:]:
        print x.index(it),'\t',it
        gotoUrl = "http://www.elaw.com/elaw21/CaseSearch.aspx"
        openUrl(gotoUrl)
        script = ("document.forms['aspnetForm'].elements['ctl00_cntData_txtNewYorkIndexYearSearch'].value='';")
        runScript(script)
    	script = ("document.forms['aspnetForm'].elements['ctl00_cntData_ddlNewYorkCounty'].value='30';"+ 
            "document.forms['aspnetForm'].elements['ctl00_cntData_txtNewYorkIndexYearSearch'].value='"+it+"';")
        runScript(script)
        script = ("document.forms['aspnetForm'].elements['ctl00_cntData_btnNYFindByIndex'].click();")
        runScript(script)
        
        script = ('document.getElementById("ctl00_cntData_ucSearch_RadGridNewYorkSearchResults_ctl00__0").innerText;')
        caps=runScript(script)
             
        script = ('document.getElementById("ctl00_cntData_ucSearch_RadGridNewYorkSearchResults_ctl00__0").innerHTML;')
        y=runScript(script)
        soup = BeautifulSoup(y)
        link=soup.a.get('href')
        openUrl(link)
        
        checkLoaded('','')
        activate()
        click()
        checkLoaded('','')
    
        try:
            script = ('document.getElementById("divFilingsAndFees").innerHTML;')
            z=runScript(script)
            soup = BeautifulSoup(z)
            t=soup.table.tbody
            tr=t("tr")
        except:
            checkLoaded('','')
            script = ('document.getElementById("divFilingsAndFees").innerHTML;')
            z=runScript(script)
            soup = BeautifulSoup(z)
            t=soup.table.tbody
            tr=t("tr")
        
        #for it in tr:
        td=tr[0]("td")
        p=td[1].em.contents[0]
        td=tr[1]("td")
        d=td[1].em.contents[0]
        
        f=open('/Users/admin/Desktop/elaw_captions.txt','a')
        f.writelines(caps+"#$#")
        f.close()
        f=open('/Users/admin/Desktop/elaw_plaintiffs.txt','a')
        f.writelines(p+"#$#")
        f.close()
        f=open('/Users/admin/Desktop/elaw_defendants.txt','a')
        f.writelines(d+"#$#")
        f.close()

def process_elaw():
    f=open('/Users/admin/Desktop/elaw_captions.txt','r')
    x=f.read()
    f.close()
    
    f=open('/Users/admin/Desktop/elaw_plaintiffs.txt','r')
    y=f.read()
    f.close()
    
    f=open('/Users/admin/Desktop/elaw_defendants.txt','r')
    z=f.read()
    f.close()
    
    #print len(x.split("#$#")),len(y.split("#$#")),len(z.split("#$#")),len(z.split("HATZEL"))
    caps,status,index=[],[],[]
    i=0
    for it in x.split("#$#")[:-1]:
        i+=1
        caps.append(it.split('\n')[0])
        status.append(it.split('\n')[1])
        index.append(it.split('\n')[2][41:52])

    hatzel=[]
    for it in z.split("#$#"):
        if it.find("HATZEL") == -1:
            hatzel.append("No")
        else:
            hatzel.append("Yes")

    var_str="Caption"+'\t'+"Status"+'\t'+"Index"+'\t'+"Hatzel"+'\t'+"Plaintiff"+'\r\n'
    v=[var_str]
    j=0
    for it in y.split("#$#"):
        for p in it.split(',')[:-1]:
            v.append(caps[j]+'\t'+status[j]+'\t'+index[j]+'\t'+hatzel[j]+'\t'+p.strip()+'\r\n')
        j+=1
    
    f=open('/Users/admin/Desktop/elaw_results.txt','w')
    for v_str in v:
        f.writelines(v_str)
    f.close()
    print len(v)


    
    

#     
#      script = ("document.forms['aspnetForm'].innerHTML")
#      c=runScript(script)
#      soup = BeautifulSoup(c)
#      d=soup('script')
#      for it in d:
#          if str(it.get('src')).find("Telerik") != -1:
#              src=it.get('src')
#              break
#      print len(d)
#      print sdfgds
#      script = ("document.forms['aspnetForm'].elements['ctl00_cntData_RTSCaseDetails_ClientState'].value="+"'"+
#                '{"selectedIndexes":["1"],"logEntries":[],"scrollState":{}}'+"';"+
#                "document.forms['aspnetForm'].elements['ctl00_cntData_RMPCaseDetail_ClientState'].value="+"'"+
#                '{"selectedIndexes":["2"],"logEntries":[],"scrollState":{}}'+"';"+
#                #ctl00_scriptLDMWO=ctl00_cntData_ctl00_cntData_RadAjaxPanelFilingsAndFeesPanel|ctl00_cntData_RadAjaxPanelFilingsAndFees&
#                #"document.forms['aspnetForm'].elements['RadAJAXControlID'].value='ctl00_cntData_RadAjaxPanelFilingsAndFees'")
#                #'ctl00_cntData_RadAjaxPanelFilingsAndFees'+"';"+
#                "document.forms['aspnetForm'].submit()")
#      runScript(script)
#     script = ("document.forms['aspnetForm'].submit()")
#     runScript(script)
    

def get_saved_pages_info(workfold):
    x = getAllFilePaths(workfold)
    
    # '''
    print '\nnumber of files:', len(x[0])
    a = []
    for it in x[0]:
        a.append(it[it.rfind('/') + 1:it.rfind('_')])

    # print a[0]
    # print a[1]
    
    names, status, b = [], [], []
    for it in a:
        # print it[7]
        # break
        # print it
        # print '------'
        # it=it.rstrip('\r')
        # it=it.rstrip('\n')
        # it=it[:-1]
        # if it[7]=='9': b=it[:6]+'-19'+it[7:]
        # else: b=it[:6]+'-20'+it[7:]
        # b=str(it)
        # print len(it)
        if b.count(it) == 0: 
            names.append(it + '_names.html')
            status.append(it + '_status.html')
            b.append(it)
    a = b
    '''
    print len(a)
    print a[0]
    print a[1]
    print names[0]
    print status[0]
    '''
    return a,names,status
def get_names(name_file):
    f = open(name_file, 'r')
    x = f.read()
    f.close()
    y = getAllTag(x, 'tr')
    p, d = [], []
    for z in y[1:]:
        j = getAllTag(z, 'td')
        if len(j) == 2:
            p1 = getAllTag(j[0], 'span')
            # print p1
            d1 = getAllTag(j[1], 'span')
            # print p2
            if p.count(str(p1[0]).strip()) == 0: p.append(str(p1[0]).strip())
            if d.count(str(d1[0]).strip()) == 0: d.append(str(d1[0]).strip())
    return p, d
    
def get_status(status_file, file_no):
    f = open(status_file, 'r')
    x = f.read()
    f.close()
    if str(x).count('THIS INDEX NUMBER COULD NOT BE FOUND') != 0: case_status = 'No Info Available'
    else:
        try : 
            if str(x).count(file_no) == 0: case_status = 'WrongFile'
        except: 
            print status_file
            print asdsa
        else:
            y = getAllTag(x, 'tr')
            try:
                j = getAllTag(y[3], 'td')
            except:
                print status_file
                print y
                print asdsa
            case_status = getAllTag(j[1], 'span')[0].strip()
        '''        
        except:
            gotoUrl='http://iapps.courts.state.ny.us/iscroll/CaseCap.jsp?IndexNo='+a[i]
            runLink(gotoUrl,a[i],workfold)
            f=open(status[i],'r')
            x=f.read()
            f.close()
            y=getAllTag(x,'tr')
            j=getAllTag(y[3],'td')
            case_status=getAllTag(j[1],'span')[0].strip()
        '''
    return case_status
def get_caption(status_file, file_no):
    f = open(status_file, 'r')
    x = f.read()
    f.close()
    if str(x).count('THIS INDEX NUMBER COULD NOT BE FOUND') != 0: case_caption = 'No Info Available'
    else:
        try : 
            if str(x).count(file_no) == 0: case_caption = 'WrongFile'
        except: 
            print status_file
            print asdsa
        else:
            y = getAllTag(x, 'div')
            y2 = getAllTag(y[3], 'font')
            case_caption = y2[0].strip()
    return case_caption
def get_names_statuses(indexNumbers, workfold, names, status):
    a = indexNumbers
    var_str = "Index No." + '\t' + 'Plaintiff' + '\t' + 'Status' + '\t' + 'Hatzel?' + '\t' + 'Goodall?'
    v = [var_str]
    z = 0
    
    # files=getAllFilePaths(workfold)
    
    
    # compare_text(x,folder1,folder1,test_var):
    # compare_names(x,names,workfold1,workfold2)
    # print asdfsa
    
    for i in range(0, len(a)):
        # try:
        # if a[i] == '102149-2005': stop=False
    
        # compare(names)
        p, d = get_names(workfold + names[i])
        # p2,d2=get_names(workfold2+names[i])
        # if p != p2: print a[i],'plaintiffs'
        # if d != d2: print a[i],'defendants'
        
        # check parties
        if str(d).lower().count('hatzel') != 0: hatzel = "Yes"
        else: hatzel = "No"
        if str(d).lower().count('gooda') != 0: goodall = "Yes"
        else: goodall = "No"
        
        # compare_status
        case_status = get_status(workfold1 + status[i], a[i])
        # case_status2=get_status(workfold2+status[i],a[i])
        # if case_status1 != case_status2: 
        #    if case_status2 == 'WrongFile': print a[i],'redo_second'
        #    else:
        #        if case_status1 == case_status2: pass
        #        else: print a[i],'not sure'
        
        # make usable data
        for j in range(0, len(p)):
            var_str = "Index No." + '\t' + 'Plaintiff' + '\t' + 'Status' + '\t' + 'Hatzel?' + '\t' + 'Goodall?'
            v.append(a[i] + '\t' + p[j] + '\t' + case_status + '\t' + hatzel + '\t' + goodall)
    
    return v
def get_all_names(indexNumbers, workfold, names):
    a = indexNumbers
    var_str = "Index No." + '\t' + 'Plaintiff' + '\t' + 'Status' + '\t' + 'Hatzel?' + '\t' + 'Goodall?'
    v = [var_str]
    z = 0
    for i in range(0, len(a)):  
        # compare(names)
        p, d = get_names(workfold + names[i])
        # p2,d2=get_names(workfold2+names[i])
        # if p != p2: print a[i],'plaintiffs'
        # if d != d2: print a[i],'defendants'
        
        # make usable data
        for j in range(0, len(p)):
            var_str = "Index No." + '\t' + 'Plaintiff'
            v.append(a[i] + '\t' + p[j]) 
    return v
def get_data_from_file(filepath):
    f = open(filepath)
    x = f.read()
    f.close()
    
    
    a = []
    x = x.replace('\n', '\r')
    x = x.replace('\r\r', '\r')
    x = x.replace('\r\r', '\r')
    x = x.split('\r')
    for i in range(0, len(x)):
        it = x[i]
        if type(it) != str:
            print type(it)
        if len(it.strip()) != 11:
            a.extend(x[i].split('\r'))
        else:
            a.append(x[i])
    
    # print a.index('106462-1995')
    # print sdfds
    b = []
    for i in range(0, len(a)):
        it = a[i]
        if len(it.strip()) != 11:
            if it == "":
                pass
            else:
                print it.count('\n')
                print '-' + it.strip() + '-'
                print dasfds
        else: b.append(a[i])
        
    '''
    #x.sort()
    print "entry",x[0]
    print "len of entry",len(x[0])
    print "last entry",x[len(x)-1]
    print 'len',len(x)
    print asdfsa
    '''
    return b
def get_data_from_file2(filePath,workfold):
    b = get_data_from_file(filepath)
    a,names,status=get_saved_pages_info(workfold)
    popList=[]
    for it in b:
        if a.count(it) != 0:
            popList.append(b.index(it))
    for it in popList:
        x=b.pop(it)
def get_all_captions(a,status):
    captions=[]
    var_str = "Index No." + '\t' + 'Captions'
    v = [var_str]
    for i in range(0,len(a)):
        x=a[i]
        y=workfold+status[i]
        v.append(a[i]+'\t'+get_caption(y,x))
    
    for it in v:
        print it

workfold = '/Users/admin/Desktop/EBG/'
workfold1 = '/Users/admin/Desktop/HB/'
workfold2 = '/Users/admin/Desktop/HB2/'
workFile='/Users/admin/Desktop/elaw_files.txt'


#f=open(workFile,'r')
#x=f.readlines()
#f.close()
#y=[]
#for it in x:
#    y.append(it.strip('\r\n'))
#scrape_elaw(y)

process_elaw()

##x=getFilesFolders(workfold,full=True)
##a=63982
##var_str="FileName"+'\t'+'BegProd'+'\t'+'EndProd'
##v=[var_str]
##for it in x:
##    d=pdfPageCount(x[0]).strip()
##    b=a+eval(d.strip(".PDF"))
##    v.append(d+'\t'+a+'\t'+b)
##    a=b+1
##for it in v: print it



# /////////
# STEP 1 -- get data from text file in usable format
# /////////


#filepath = '/Users/admin/Desktop/to_check_04.08.txt'
#b=get_data_from_file(filePath)

#a,b=getAllFilePaths(workfold)[0],[]
#for it in a:
#    x=it.strip("_status.html")
#    y=it.strip("_names.html")
#    if len(x) > len(y):
#        if b.count(y) == 0:
#            b.append(y)


#a,names,status=get_saved_pages_info(workfold)
#get_all_captions(a,status)


# print len(b)
# print b[196],b[197],b[198]
# print b.index('122169-1995')
# print dsfsad

# /////////
# STEP 2 -- get webpages with data
# /////////

#b.reverse()
# test scrape
# x=[b[0]]
#scrape_pages(b, workfold)

# /////////
# STEP 3 -- extract data from saved webpages
# /////////

#a,names,status=get_saved_pages_info(workfold)
#x=get_names_statuses(a,workfold,names,status)
#x=get_all_names(a,workfold,names)
show = False

if show == True:
    for j in x:
        print j
    

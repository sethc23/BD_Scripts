'''
Created on Nov 10, 2013

@author: sethchase
'''
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from API_system import get_pwd,exec_cmd
from webpage_scrape import scraper
from HTML_API import getSoup,FindAllTags,getTagsByAttr,getInnerElement,getTagContents



def copy_Ports_MBP_to_MB(MBP_filePath='',MB_filePath=''):
    pwd=get_pwd()
    
    if (MBP_filePath == '' or MB_filePath == ''):
        MB_filePath=pwd.rstrip('/')+'/MB_ports.txt'
        MBP_filePath='/Users/admin/Desktop/MBP.txt'
#         newPortPath=pwd.rstrip('/')+'/MB_newPorts.txt'
    
    cmd = 'port -qv installed > '+MB_filePath
    exec_cmd(cmd)
    
    f=open(MB_filePath,'r')
    x=f.read()
    f.close()
    x=x.split('\n')
    
    f=open(MBP_filePath,'r')
    y=f.read()
    f.close()
    y=y.split('\n')
    
    z,z2='',[]
    
    skip=['py25-html5lib','py25-lxml','py25-beautifulsoup4']
    for it in y:
        next=False
        if (x.count(it)==0 and it.find('(active)')!=-1):
            next=True
            newIt=it[:it.find('(active)')-1].strip()
        if next == True:
            for mod in skip:
                if newIt.find(mod)!=-1:
                    next=False
                    break
        if next == True:
            if z2.count(newIt) == 0:
                z+=newIt+'\n'
                z2.append(newIt)
    
    for it in z2:
        cmd = 'echo money | sudo -S port install '+it
        exec_cmd(cmd)
    
    print len(z2),'ports installed'


#update()

def get_MBP_IPs():
    br=scraper('urllib2').browser
    a=br.get_page('http://www.sanspaperllc.com/seth/settings.xml')
    MBP_IP_int=FindAllTags(a,'row')[0].get('address')
    MBP_IP_ext=FindAllTags(a,'row')[1].get('address')
    # print type(z.contents),z.contents
    # b=getSoup(a)
    # print b('ADDRESS')[0].contents
    # tags=getTagsByAttr(a,'row', attr='',contents=True)
    # # print tags
    # MBP_IP_ext=getTagContents(a, 'row', 'ADDRESS')
    return MBP_IP_int, MBP_IP_ext

''==''

#def update_macports():

# int,ext=get_MBP_IPs()
# 
fromComp='/Users/admin/SERVER2/BD_Scripts/files_folders/MBP_ports.txt'
toComp='/Users/admin/SERVER2/BD_Scripts/files_folders/MB_ports.txt'
 
# MBP_cmd1 = ('sshpass -p money '+'ssh sethchase@'+str(ext)+' '+
#         'port -qv installed > '+fromComp)
# MBP_cmd2 = ('sshpass -p money '+'scp sethchase@'+str(ext)+' '+
#         fromComp+' '+
#         '/Users/admin/SERVER2/BD_Scripts/files_folders/')

# exec_cmd(MBP_cmd1)
# try:
#     exec_cmd(MBP_cmd2)
# except:
#     print 'MBP file already up-to-date'
#     raise SystemExit
 
MB_cmd1 = 'port -qv installed > '+toComp
exec_cmd(MB_cmd1)

copy_Ports_MBP_to_MB(fromComp,toComp)



''
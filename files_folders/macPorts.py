'''
Created on Nov 10, 2013

@author: sethchase
'''
#from sys import path
#path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import get_pwd,exec_cmd

#def update(from_comp='',to_comp=''):
pwd=get_pwd()

MB_filePath=pwd.rstrip('/')+'/MB_ports.txt'
MBP_filePath='/Users/admin/Desktop/MBP.txt'
newPortPath=pwd.rstrip('/')+'/MB_newPorts.txt'

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
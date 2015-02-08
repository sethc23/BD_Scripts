from sys import argv, path
path.append('$HOME/Dropbox/Scripts')
path.append('$HOME/Dropbox/Scripts/crons')
path.append('$HOME/Dropbox/Scripts/gmail')
path.append('$HOME/Dropbox/Scripts/finance')
from os import system, getcwd
from datetime import datetime
from manage_cron import updateCrons

def workDirPath():
    return '/Users/admin/SERVER2/BD_Scripts/crons'

def createTestFile():
    workDir = workDirPath()
    cmd = 'echo "test" > ' + workDir + '/cronsTest.txt'
    system(cmd)
    

if __name__ == '__main__':
    # print str(time.localtime()[3])+':'+str(time.localtime()[4])
    createTestFile()
    updateCrons('cronTest.py')
    
    


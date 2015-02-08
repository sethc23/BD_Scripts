from sys import argv, path
path.append('$HOME/Dropbox/Scripts')
path.append('$HOME/Dropbox/Scripts/crons')
path.append('$HOME/Dropbox/Scripts/gmail')
path.append('$HOME/Dropbox/Scripts/finance')
from os import system, getcwd
from datetime import datetime

def workDirPath():
    return '/Users/admin/SERVER2/BD_Scripts/crons'

def runStop():
    workDir = workDirPath()
    cronStatus = 'cronsManagerStatus.txt'
    today = str(datetime.today().timetuple()[:-6])[1:-1]
    f = open(workDir + '/' + cronsToday_file, 'w')
    f.write(today)
    f.close()

def updateCrons(script):   
    workDir = workDirPath()
    cronsToday_file = 'cronsToday.txt'
    now = str(datetime.today().timetuple()[:-6])[1:-1]
    text = now + ' -- ' + script
    cmd = 'echo "' + text + '" >> ' + workDir + '/' + cronsToday_file    
    system(cmd)
    checkCrons()

def stopCrons():
    workDir = workDirPath()
    cmd = 'echo "" > ' + workDir + '/' + 'cron.txt'
    system(cmd)
    cmd = 'crontab ' + workDir + '/cron.txt'
    system(cmd)

def updateManager(dateStr):
    workDir = workDirPath()
    cronStatus_file = 'cronStatus.txt'
    cmd = 'echo "' + dateStr + '" > ' + workDir + '/' + cronStatus_file
    system(cmd)
    

def checkManager():
    workDir = workDirPath()
    cronStatus_file = 'cronStatus.txt'
    f = open(workDir + '/' + cronStatus_file, 'r')
    status = f.read()
    f.close()
    return status

def runCheck():
    workDir = workDirPath()
    # get crons executed today
    cronsToday = 'cronsToday.txt'
    f = open(workDir + '/' + cronsToday, 'r')
    jobs = f.readlines()
    f.close()
    # create list of crons that were executed today and clear list of old crons
    if len(jobs) == 0:
        ignore_crons = []
    else:
        ignore_crons, lastCrons = [], [] 
        today = datetime.today()
        for it in jobs:
            var_date, cronjob = it.split('--')[0].strip(), it.split('--')[1].strip()
            lastRun = datetime.strptime(var_date, '%Y, %m, %d')
            if (today - lastRun).days == 0:
                lastCrons.append(it)
                ignore_crons.append(cronjob)
        if lastCrons != []:
            f = open(workDir + '/' + cronsToday, 'w')
            for it in lastCrons: 
                f.writelines(it)
            f.close()
                
    '''
    #get list of scheduled cron, add to ignore list
    crontab=getCrontab()
    if len(crontab) == 0:
        pass
    else:
        for it in crontab:
            m=it.rfind('.py')
            job=it[it[:m].rfind('/')+1:m+3].rstrip('\n')
            if job ???
    '''        
    # get all crons that are suppose to be executed
    cronJobs_file = 'cronCmds.txt'
    f = open(workDir + '/' + cronJobs_file, 'r')
    cronJobs = f.readlines()
    f.close()
    # make list of crons that will be executed today
    if len(ignore_crons) == 0:
        return cronJobs
    elif len(cronJobs) == 0:
        return cronJobs
    else:
        
        runCrons = []
        for it in cronJobs:
            m = it.rfind('.py')
            job = it[it[:m].rfind('/') + 1:m + 3].rstrip('\n')
            job = job.replace(' ', '')
            if ignore_crons.count(job) == 0:
                runCrons.append(it)
        return runCrons

def checkCrons():
    today = str(datetime.today().timetuple()[:-6])[1:-1]
    # get last date cron_manager completed jobs (if today, then end check)
    if checkManager() == today:
        return
    workDir = workDirPath()
    # get crons executed today
    # create list of crons that were executed today and clear list of old crons
    # get all crons that are suppose to be executed
    # make list of crons that will be executed today
    # return jobs left for today
    runCrons = runCheck()
    if len(runCrons) == 0:
        today = str(datetime.today().timetuple()[:-6])[1:-1]
        updateManager(today)
    else:
        crontab = []
        for i in range(0, len(runCrons)):
            time = 'date -v+' + str(2 + (15 * i)) + 'M "+%M %H * * * ' + runCrons[i] + '"'
            crontab.append(time)
        sendCrons(crontab)
    verifyManagerCron()

# check to make sure manager_cron.py is scheduled to run
def verifyManagerCron():
    workDir = workDirPath()
    f = open(workDir + '/cronregulars.txt', 'r')
    crons = f.read().replace('\r', '\n').split('\n')
    crontab = getCrontab()
    change = False
    for it in crons:
        if crontab.count(it) == 0:
            crontab.append(it)
            change = True
    if change == True:
        sendCrons(crontab, True)

def getCrontab():
    workDir = workDirPath()
    crontab_file = 'crontab.txt'
    cmd = 'crontab -l > ' + workDir + '/' + crontab_file
    crontab = system(cmd)
    f = open(workDir + '/' + crontab_file, 'r')
    crontab = f.read()
    f.close()
    crontab = crontab.split('\n')
    for it in crontab:
        if it == "":
            crontab.pop(crontab.index(it))
    return crontab

def sendCrons(cron_list, exact=False):
    workDir = workDirPath()
    if cron_list[0] != "":
        cmd = cron_list[0] + ' > ' + workDir + '/cron.txt'
        if exact == True:
            cmd = 'echo "' + cron_list[0] + '" > ' + workDir + '/cron.txt'
        system(cmd)
    if len(cron_list) > 1:
        for i in range(1, len(cron_list)):
            if cron_list[i] != "":
                cmd = cron_list[i] + ' >> ' + workDir + '/cron.txt'
                if exact == True:
                    cmd = 'echo "' + cron_list[i] + '" >> ' + workDir + '/cron.txt'
                system(cmd)
    cmd = 'crontab ' + workDir + '/cron.txt'
    system(cmd)

        

if __name__ == '__main__':
    # print str(time.localtime()[3])+':'+str(time.localtime()[4])

    try:
        task = argv[1]
        stop = False
    except:
        print 'argument error'
        stop = True

    #-------
    # --Testing Grounds--#
    #-------
    # stop=False
    # task='run'
    # x=runCheck()
    # print x
    # updateCrons('gmail_tasks.sh')
    # runCheck()
    # runStop()
    # updateCrons('gmail_tasks.py')
    # managerStatus()
    # checkCrons()
    #-------
    
    if stop == False:
        if task == 'run':
            checkCrons()
        if task == 'stopAll':
            stopCrons()
            


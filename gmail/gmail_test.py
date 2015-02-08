from sys import argv, path
path.append('/Users/admin/SERVER2/BD_Scripts')
path.append('/Users/admin/SERVER2/BD_Scripts/crons')
path.append('/Users/admin/SERVER2/BD_Scripts/gmail')
path.append('/Users/admin/SERVER2/BD_Scripts/finance')
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from time import time, mktime
from datetime import datetime
from manage_cron import updateCrons

import gmail_tasks
import gmail_imap
import sortListArray, listFout, listFin

def clean_date(msg_date): 
    try:
        msg_date = msg_date.lower()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday',
                  'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', ]
        for it in weekdays:
            msg_date = msg_date.replace(it, '')
        msg_date = msg_date.replace(',', '')
        long_months = ['january', 'february', 'march', 'april',
                     'may', 'june', 'july', 'august',
                     'september', 'october', 'november', 'december']
        short_months = ['jan', 'feb', 'mar', 'apr',
                     'may', 'jun', 'jul', 'aug',
                     'sep', 'oct', 'nov', 'dec']
        for it in long_months:
            msg_date = msg_date.replace(it, short_months[long_months.index(it)])       
        if (msg_date.find('+') != -1 or msg_date.find('-') != -1):
            if msg_date[msg_date.find('+') + 4].isdigit():
                msg_date = msg_date[:msg_date.find('+') - 1]
            if msg_date[msg_date.find('-') + 4].isdigit():
                msg_date = msg_date[:msg_date.find('-') - 1]              
        msg_date = msg_date.strip()

        if len(msg_date.split()[2]) == 2:
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            for it in months:
                if msg_date.find(it) != -1:
                    a = msg_date[msg_date.find(it) + len(it):msg_date.find(':') - 3]
                    a = a.strip().replace(' ', '')
                    if len(a) == 2:
                        msg_date = msg_date[:msg_date.find(it) + len(it) + 1] + '20' + msg_date[msg_date.find(it) + len(it) + 1:]
                            
        if msg_date.count(':') == 2:
            msgDate = datetime.strptime(msg_date[:msg_date.rfind(":") + 3], '%d %b %Y %H:%M:%S')
        elif msg_date.count(':') == 1:
            msgDate = datetime.strptime(msg_date[:msg_date.rfind(":") + 3], '%d %b %Y %H:%M')

        return msgDate

    except:  
        print 'date error (in clean_communications)'
        print msg_date
        return

def getPhoneCommunications(comm_msgs, log_sources):
    uniq_msgs = [], []
    msg_refs = []
    stop = False
    for it in log_sources:
        if stop == True:
            break
        gmail.messages.process(it, 'all')
        msg_folder = it
        for msg in gmail.messages:
            if comm_msgs[8].count(msg.msgID) == 0:
                msg_date = clean_date(msg.date)
                msg_date = msg_date.strftime('%Y.%m.%d_%H:%M')

                from_msg_name, from_msg_source = '', ''
                to_msg_name, to_msg_source = '', ''
                var = [msg.From, msg.To]
                for it in var:
                    if str(it) != "None":
                        if it.find('<') != -1:
                            msg_name = it[:it.find('<') - 1].strip('"')
                            msg_source = it[it.find('<') + 1:it.find('>')]
                        else:
                            msg_name, msg_source = it, it
                        msg_name = msg_name.replace('<', '').replace('>', '')
                        msg_name = ' '.join(str(n) for n in [x.capitalize() for x in msg_name.split()])
                        if var.index(it) == 0:
                            from_msg_name = msg_name
                            from_msg_source = msg_source
                        if var.index(it) == 1:
                            to_msg_name = msg_name
                            to_msg_source = msg_source
                
                comm_msgs[0].append(msg_folder)
                comm_msgs[1].append(msg.uid)
                comm_msgs[2].append(msg_date)
                comm_msgs[3].append(from_msg_name)
                comm_msgs[4].append(from_msg_source)
                comm_msgs[5].append(to_msg_name)
                comm_msgs[6].append(to_msg_source)            
                comm_msgs[7].append(msg.ReplyTo)
                comm_msgs[8].append(msg.msgID)

                if msg.From.find('seth.t.chase') == -1 or msg.From.find('Me') == -1:
                    msg_name = from_msg_name
                elif msg.To.find('seth.t.chase') == -1 or msg.From.find('Me') == -1:
                    msg_name = to_msg_name
                
                msg_name = ' '.join(str(n) for n in [x.capitalize() for x in msg_name.split()])
                    
                if uniq_msgs[1].count(msg_name) == 0:
                    uniq_msgs[1].append(msg_name)
                    
                for it in [msg.msgID, msg.ReplyTo]:
                    if msg_refs.count(it) == 0 and it != '' and it != None:
                        msg_refs.append(it)  

            # if len(comm_msgs[0])>=50:
            #    break
            
    return comm_msgs, uniq_msgs, msg_refs

def getEmailsForPhoneContacts(comm_msgs, uniq_msgs, msg_refs, item_list):
    stop = False
    for box in item_list:
        if stop == True:
            break
        headers = gmail.messages.process(box, 'all')
        # texts=gmail.messages.fetch(box,'body')
        # gmail.messages.searchBox(box,'HEADER',uniq_msgs[1])
        # print len(gmail.messages)

        for msg in headers:
            add = False
            skip = False
            
            from_msg_name = ''
            from_msg_source = ''
            to_msg_name = ''
            to_msg_source = ''

            msg_date = clean_date(msg.date)
            msg_date = msg_date.strftime('%Y.%m.%d_%H:%M')

            a = [uniq_msgs[0][0], msg_date]
            a.sort()
            if a.index(msg_date) == 0:
                skip = True

            if comm_msgs[8].count(msg.msgID) != 0:
                skip = True
                
            if skip == False:
                for it in [msg.msgID, msg.ReplyTo]:  # note: this is after above check for same msg.msgID
                    if msg_refs.count(it) != 0:
                        add = True
                        break
                ##------------------
                var = [msg.From, msg.To]
                for it in var:
                    if str(it) != "None":
                        if it.find('<') != -1:
                            msg_name = it[:it.find('<') - 1].strip('"')
                            msg_source = it[it.find('<') + 1:it.find('>')]
                        else:
                            msg_name, msg_source = it, it
                        msg_name = msg_name.replace('<', '').replace('>', '')
                        msg_name = ' '.join(str(n) for n in [x.capitalize() for x in msg_name.split()])
                        if var.index(it) == 0:
                            from_msg_name = msg_name
                            from_msg_source = msg_source
                        if var.index(it) == 1:
                            to_msg_name = msg_name
                            to_msg_source = msg_source
                        if uniq_msgs[1].count(msg_name) != 0:
                            add = True

            if add == True:
                comm_msgs[0].append(msg.mailbox)
                comm_msgs[1].append(msg.uid)
                comm_msgs[2].append(msg_date)
                comm_msgs[3].append(from_msg_name)
                comm_msgs[4].append(from_msg_source)
                comm_msgs[5].append(to_msg_name)
                comm_msgs[6].append(to_msg_source)            
                comm_msgs[7].append(msg.ReplyTo)
                comm_msgs[8].append(msg.msgID)

                for it in [msg.msgID, msg.ReplyTo]:
                    if msg_refs.count(it) == 0 and it != '' and it != None:
                        msg_refs.append(it)
                
            if len(comm_msgs[0]) >= 7000:
                stop = True
                break
            
    return comm_msgs, uniq_msgs, msg_refs

    
def getMessageBody():
    pass
    '''
        if len(comm_msgs[0]) != len(comm_msgs[7]):
            uidList=comm_msgs[1][len(comm_msgs[7]):]
            if len(uidList) < 11:
                x=gmail.messages.fetchUIDs(box,uidList,'body')
                for body in x:
                    comm_msgs[7].append(body)
            else:
                for i in range(0,(len(uidList)/5)+1):
                    tmpList=uidList[-5:]
                    uidList=uidList[:len(uidList)-len(tmpList)]
                    x=gmail.messages.fetchUIDs(box,tmpList,'body')
                    for body in x:
                        comm_msgs[7].append(body)
                    if len(uidList) == 0:
                        break
'''


def printRow(comm_msgs, num):
    print ''
    for i in range(0, len(comm_msgs)):
        print comm_msgs[i][num]
    print ''


##----------------------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------------------

"""
comm_msgs[0].append(msg_folder)
comm_msgs[1].append(msg.uid)
comm_msgs[2].append(msg_date)
comm_msgs[3].append(from_msg_name)
comm_msgs[4].append(from_msg_source)
comm_msgs[5].append(to_msg_name)
comm_msgs[6].append(to_msg_source)            
comm_msgs[7].append([msg.msgID,msg.msgRef,msg.ReplyTo])
comm_msgs[8].append(msg.Body)

uniq_msgs[0]=uniq_type
uniq_msgs[1]=uniq_val
uniq_msgs[2]=msg.msgID,msg.msgRef,msg.ReplyTo

"""


#------
# #get all SMS and call logs
# #
#------
print '-'

gmail = gmail_imap.gmail_imap('seth.t.chase', 'F*rrari1')
gmail.mailboxes.load()


'''
comm_msgs=[]
for i in range(0,9):
    comm_msgs.append([])

log_sources=['SMS','Call log']
comm_msgs,uniq_msgs,msg_refs = getPhoneCommunications(comm_msgs,log_sources)
print 'first comm_msgs=',len(comm_msgs[0]),' = ',len(comm_msgs[8])
print 'first uniq_dates=',len(uniq_msgs[0])
print 'first uniq_names=',len(uniq_msgs[1])
print 'first msg_refs=',len(msg_refs)
print '--'

#------
##remove from uniq and comm_msgs, values that are unlikely contacts
##
#------

exclude_name=['Me','Seth Chase']
for it in exclude_name:
    if uniq_msgs[1].count(it) != 0:
        uniq_msgs[1].pop(uniq_msgs[1].index(it))

poplist=[]
for i in range(0,len(uniq_msgs[1])):
    if len(uniq_msgs[1][i]) < 3:
        poplist.append(i)
poplist.reverse()
comm_poplist=[]

for it in poplist:
    if str(it).isalpha() == False or str(it).isdigit() == True:
        x=uniq_msgs[1].pop(it)
        print x
        break
    if x != '':
        for i in range(0,3):  ##for each column
            if comm_msgs[i].count(x) != 0:  ##if found in column
                y=comm_msgs[i].count(x)
                pt=0
                for j in range(0,y-1):
                    if comm_poplist.count(comm_msgs[i][pt:].index(x)) == 0:
                        comm_poplist.append(comm_msgs[i][pt:].index(x))
                    if y>1:
                        pt=comm_msgs[i][pt:].index(x)+1
comm_poplist.sort()
comm_poplist.reverse()
for it in comm_poplist:
    for i in range(0,len(comm_msgs)):
        x=comm_msgs[i].pop(it)
        if i == len(comm_msgs)-1:
            for ref in x:
                if msg_refs.count(ref) != 0:
                    y=msg_refs.pop(msg_refs.index(ref))
print 'comm_poplist =',len(comm_poplist)
print 'after pop uniq_dates=',len(uniq_msgs[0])
print 'after pop uniq_names=',len(uniq_msgs[1])
print 'after pop comm_msgs=',len(comm_msgs[0]),' = ',len(comm_msgs[8])
print 'after pop msg_refs=',len(msg_refs)
print '---'

#------
##get oldest date of unique SMS or call log
##
#------

for it in uniq_msgs[1]:
    msg_pt=''
    pt=uniq_msgs[1].index(it)
    name_lists=[3,5]
    for i in name_lists:
        if comm_msgs[i].count(it) != 0:
            msg_pt=comm_msgs[i].index(it)
            break
    if msg_pt != '':
        uniq_msgs[0].append(comm_msgs[2][msg_pt])
c=[uniq_msgs[0],uniq_msgs[1]]
uniq_msgs=sortListArray.sortListArray(c,0)
print 'second uniq_dates=',len(uniq_msgs[0])
print 'first uniq_names=',len(uniq_msgs[1])
print '----'

#------
##get emails from those contacts with phone communications
##
#------

exclude_list=['_MATCHED','Blocked','Call log','INBOX','SMS','_DRAFTS','BANK','COMMUNICATIONS']
archive_list=['LAW/PATENT','WEB','WEB/CONFIRMATIONS','WEB/DOMAINS',
              'WEB/GOOGLE','WEB/HOSTING','WEB/TECHNOLOGY',
              '_INBOX_SansPaper/AIIM','_INBOX_SansPaper/Conf_Calls']
gmail.mailboxes.load()
all_box=gmail.mailboxes        
item_list=[]
for it in all_box:
    if (archive_list.count(it) == 0 and exclude_list.count(it) == 0):
        if item_list.count(it) == 0:
            item_list.append(it)

comm_msgs,uniq_msgs,msg_refs = getEmailsForPhoneContacts(comm_msgs,uniq_msgs,msg_refs,item_list)
print 'second comm_msgs=',len(comm_msgs[0]),' = ',len(comm_msgs[8])
print 'second uniq_msgs=',len(uniq_msgs[0]),' = ',len(uniq_msgs[1])
print 'second msg_refs=',len(msg_refs)
print '-----'

'''
#------
# #create groups of communications
# #
#------
   
"""
-
first comm_msgs= 5818  =  5818
first uniq_dates= 0
first uniq_names= 130
first msg_refs= 5818
--
-2
comm_poplist = 0
after pop uniq_dates= 0
after pop uniq_names= 128
after pop comm_msgs= 5818  =  5818
after pop msg_refs= 5818
---
second uniq_dates= 128
first uniq_names= 128
----
second comm_msgs= 6414  =  6414
second uniq_msgs= 128  =  128
second msg_refs= 6434
-----
"""
"""
listFout.listFout(comm_msgs,'comm_msgs.txt')
listFout.listFout(uniq_msgs,'uniq_msgs.txt')
listFout.listFout(msg_refs,'msg_refs.txt')
"""
# """
comm_msgs = listFin.listFin('comm_msgs.txt')
uniq_msgs = listFin.listFin('uniq_msgs.txt')
msg_refs = listFin.listFin('msg_refs.txt')
# """

stop = False
comm_list = eval(comm_msgs.__repr__())
main_comm_group = []

for it in uniq_msgs[1]:
    if stop == True:
        break
    comm_group = []
    for i in range(0, len(comm_msgs)):
        comm_group.append([])
    group_refs = []
    name_lists = [5, 3]
    for i in name_lists:
        if comm_list[i].count(it) != 0:
            comm_list = sortListArray.sortListArray(comm_list, i) 
            x = eval(comm_list[i].__repr__())
            x.sort()
            l_index = x.index(it)
            x.reverse()
            r_index = x.index(it)
            x.reverse()

            ind_nums = range(l_index, len(x) - r_index)
            ind_nums.reverse()

            for num in ind_nums:
                for j in range(0, len(comm_list)):
                    a = comm_list[j].pop(num)
                    comm_group[j].append(a)
                    if j == 7 or j == 8:
                        if group_refs.count(a) == 0 and a != None:
                            group_refs.append(a)              

    # # add based on references
    # """
    # print 'before ref comms=',len(comm_list[0])
    ind_nums = []
    for ref in msg_refs:
        if group_refs.count(ref) != 0:
            if comm_list[7].count(ref) != 0:
                pt = 0
                for j in range(0, comm_list[7].count(ref)):
                    ind = group_refs[pt:].index(ref)
                    pt += ind + 1
                    if ind_nums.count(ind) == 0:
                        ind_nums.append(ind)
            if comm_list[8].count(ref) != 0:
                pt = 0
                for j in range(0, comm_list[8].count(ref)):
                    ind = group_refs[pt:].index(ref)
                    pt += ind + 1
                    if ind_nums.count(ind) == 0:
                        ind_nums.append(ind)

    # print len(ind_nums)
    for num in ind_nums:
        for j in range(0, len(comm_list)):
            a = comm_list[j].pop(num)
            comm_group[j].append(a)
            if j == 7 or j == 8:
                if group_refs.count(a) == 0 and a != None:
                    group_refs.append(a)   

    
    # print 'after ref comms=',len(comm_list[0]),' = ',len(comm_refs[0])
    # """

    main_comm_group.append(comm_group)

print 'main_comm_group= ', len(main_comm_group)
print 'remaining comm_list= ', len(comm_list[0])
print '-------'
for i in range(0, len(comm_list[0])):
    print comm_list[0][i], comm_list[2][i], comm_list[3][i], comm_list[5][i]
'''
x1,x2,x3,x4=[],[],[],[]
for i in range(0,len(comm_list[0])):
    x1.append(comm_group[0][i])
    x2.append(comm_group[2][i])
    x3.append(comm_group[3][i])
    x4.append(comm_group[5][i])
test=[x1,x2,x3,x4]
#test=sortListArray.sortListArray(test,0)

for i in range(0,30):
    print test[0][i],test[1][i],test[2][i],test[3][i]
    
'''

"""
rowCount=0
for grp in comm_group:
    for col in grp:
        rowCount+=len(col)
print len(comm_msgs)*len(comm_msgs[0]),' = ',rowCount,' != ',len(comm_list)*len(comm_list[0])
print len(uniq_msgs[1]),' = ',len(comm_group)

for it in comm_group[0]:
    print it[3]
"""
"""
comm_msgs[0].append(msg_folder)
comm_msgs[1].append(msg.uid)
comm_msgs[2].append(msg_date)
comm_msgs[3].append(from_msg_name)
comm_msgs[4].append(from_msg_source)
comm_msgs[5].append(to_msg_name)
comm_msgs[6].append(to_msg_source)            
comm_msgs[7].append([msg.msgRef,msg.ReplyTo])
comm_msgs[8].append(msg.msgID)

uniq_msgs[0]=uniq_type
uniq_msgs[1]=uniq_val
"""

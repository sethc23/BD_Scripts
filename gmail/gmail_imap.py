import imaplib
import gmail_mailboxes, gmail_messages, gmail_message, gmail_attachments

import time
from datetime import datetime



class gmail_imap:

    def __init__ (self, username, password):
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.username = username
        self.password = password
        self.loggedIn = False
        
        self.mailboxes = gmail_mailboxes.gmail_mailboxes(self)
        self.messages = gmail_messages.gmail_messages(self)
        self.attachments = gmail_attachments.gmail_attachments(self)

        self.mailbox = ""
        self.msgData = ""
        
    def login (self):
        self.imap_server.login(self.username, self.password)
        self.loggedIn = True

    def update_matched(self):
        pass

    def logout (self):
        self.imap_server.close()
        self.imap_server.logout()
        self.loggedIn = False
        

        
if __name__ == '__main__':
    pass
    '''
    #import getpass
    #gmail = gmail_imap(getpass.getuser(),getpass.getpass())
    gmail = gmail_imap("seth.t.chase","#password#")
    
    gmail.mailboxes.load()
    all_box=gmail.mailboxes

    global_list=['_INBOX','_INBOX_UNH']
    dates,titles,uids=[],[],[]
    global_msg=dates,titles,uids,[],[]

    exclude_list=['_MATCHED','_SENT_MAIL','_SENT_OTHER','[Gmail]/Sent Mail','[Gmail]/Trash',
                  '_DRAFTS','SMS','Trash','Blocked','Call log']
    
    archive_list=['LAW/PATENT','WEB','WEB/CONFIRMATIONS','WEB/DOMAINS',
                  'WEB/GOOGLE','WEB/HOSTING','WEB/TECHNOLOGY','_CHATS',
                  '_INBOX_SansPaper/AIIM','_INBOX_SansPaper/Conf_Calls']
    
    item_list=[]
    for it in all_box:
        if (global_list.count(it) == 0 and exclude_list.count(it) == 0):
            item_list.append(it)

    for box in global_list:
        #box='_INBOX'
        gmail.messages.process(box,'all')
        for msg in gmail.messages:
            msgID=msg.msgID
            try:
                if msg.date.rfind(':') == len(msg.date)-3:
                    msgDate=datetime.strptime(msg.date,'%a, %d %b %Y %H:%M:%S')
                else:
                    msgDate=datetime.strptime(msg.date[:msg.date.rfind(':')+msg.date[msg.date.rfind(':'):].find(' ')],'%a, %d %b %Y %H:%M:%S')
            except:
                msgDate=datetime.strptime(msg.date[:msg.date.rfind(':')+msg.date[msg.date.rfind(':'):].find(' ')],'%d %b %Y %H:%M:%S')
            if (daysBack >= time.mktime(msgDate.timetuple()) or #days ago is bigger or equal to msg seconds
                archive_list.count(msg.mailbox) != 0): 
                date=msgDate.strftime('%d-%b-%Y')
                field_header='DATE "'+msg.date+'"'+' SUBJECT "'+msg.Subject+'"'
                msgID_header='Message-ID "'+msgID+'"'
                uid=msg.uid
                global_msg[0].append(msgID)
                global_msg[1].append(field_header)
                global_msg[2].append(msgID_header)
                global_msg[3].append(uid)
                global_msg[4].append(box)

    del_list=[],[]

    for boxes in item_list:
        #boxes='LAW/PATENT'
        box_msgs = gmail.messages.process(boxes,'msgID')
        if box_msgs != '[]':
            for item in global_msg[0]:
                if box_msgs.count(item) != 0:
                    index_num=global_msg[0].index(item)
                    global_msg[0].pop(index_num)
                    global_msg[1].pop(index_num)
                    global_msg[2].pop(index_num)
                    del_list[0].append(global_msg[3].pop(index_num))
                    del_list[1].append(global_msg[4].pop(index_num))
    #print del_list
    for box in global_list:
        new_del_list=[]
        for it in del_list[1]:
            index_num=del_list[1].index(it)
            if it == box:
                new_del_list.append(del_list[0].pop(index_num))
                junk=del_list[1].pop(index_num)
        
        #for i in range(0,len(del_list[1])):
        #    if del_list[1][i] == box:
        #        new_del_list.append(del_list[0][i])

        if new_del_list != []:
            gmail.messages.delMessage(box,new_del_list)

    for uid in del_list[0]:
        index_num=del_list[0].index(uid)
        gmail.messages.get(del_list[1][index_num])
        print gmail.messages.getMessage(uid)

    #print str(time.localtime()[3])+':'+str(time.localtime()[4])

    gmail.logout()
    '''    


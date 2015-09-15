import email, string, re
from email.parser import HeaderParser
import gmail_imap, gmail_mailboxes, gmail_message
import os

class gmail_messages:
    
    def __init__(self, gmail_server):
        self.server = gmail_server
        self.mailbox = None
        self.messages = list()
        self.fetch_list = ''
    

    def parseFlags(self, flags):
        return flags.split()  # Note that we don't remove the '\' from flags, just split by space
    

    def parseMetadata(self, entry):
        if(not getattr(self, 'metadataExtracter', False)):  # Lazy initiation of the parser
            self.metadataExtracter = re.compile(r'(?P<id>\d*) \(UID (?P<uid>\d*) FLAGS \((?P<flags>.*)\)\s')  
            #  I hate regexps.
            #  (\d*) = MSG ID,  the position index of the message in its mailbox
            #  \(UID (\d*) = MSG UID, the unique id of this message within its mailbox
            #  FLAGS \((.*)\)\s = MSG FLAGS, special indicators like (\Starred, \Seen) may be empty
                    # example:  55 (UID 82 FLAGS (\Seen) BODY[HEADER.FIELDS (SUBJECT FROM)] {65}
                    #               groupdict() = { id:'55', uid:'82', flags:'\\Seen' }        
        
        metadata = self.metadataExtracter.match(entry).groupdict() 
        metadata['flags'] = self.parseFlags(metadata['flags'])
        return metadata
    

    def parseHeaders(self, entry):
        if(not getattr(self, 'headerParser', False)):
            self.headerParser = HeaderParser()  # See http://docs.python.org/library/email.parser.html#parser-class-api
        
        headers = self.headerParser.parsestr(entry)
        return headers

    def selectMailbox(self, mailbox):
        if(not self.server.loggedIn):
            self.server.login()
            
        self.server.imap_server.select(mailbox, readonly=1)
        self.mailbox = mailbox
        self.messages = list()
        
        result, message = self.server.imap_server.select(mailbox, readonly=1)
        return self.mailbox

    def tell(self):
        return self.mailbox

    def fetch(self, mailbox, var):
        if self.fetch_list != "":
            f = self.server.imap_server.fetch(self.fetch_list, '(UID FLAGS BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE MESSAGE-ID REFERENCES IN-REPLY-TO)])') 
            if var == 'all_body':
                f2 = self.server.imap_server.fetch(self.fetch_list, '(UID FLAGS BODY[TEXT])')
            if var == 'all_attachments':
                f2 = self.server.imap_server.fetch(self.fetch_list, '(UID FLAGS BODYSTRUCTURE)')
                a_pt = 0
            msgIDs = []
            for fm in f[1]:
                pt = f[1].index(fm)
                if(len(fm) > 1):
                    metadata = self.parseMetadata(fm[0])  # metadata is contained 
                    headers = self.parseHeaders(fm[1])
                    # body = self.parseHeaders(fm[2])
                    msgIDs.append(headers['Message-ID'])
                    if var == 'all' or var == 'all_body' or var == 'all_attachments':
                        message = gmail_message.gmail_message()
                        message.id = metadata['id']
                        message.uid = metadata['uid']
                        message.flags = metadata['flags']
                        message.mailbox = mailbox  # UID depends on mailbox location, so we need to know which owns the message
                        message.msgID = headers['Message-ID']
                        message.msgRef = headers['References']
                        message.ReplyTo = headers['In-Reply-To']                                           
                        message.date = headers['Date']
                        message.From = headers['From']
                        message.To = headers['To']
                        if var == 'all_attachments': 
                            x = f2[1][a_pt]
                            a_pt += 1
                            s = x.find('FILENAME') + len('FILENAME') + 2
                            s1 = x.find('"', s) + 1
                            s2 = x.find('"', s1)
                            message.attachments = x[s1:s2]
                        if var == 'all_body':
                            message.Body = f2[1][pt][1]
                        if('Subject' in headers):
                            message.Subject = headers['Subject']
                        self.messages.append(message)
                        # """
            if var == 'msgID':
                return msgIDs
        else:
            return False
        
    

    def fetchUIDs(self, mailbox, uid_list, var):
        if self.mailbox == "":
            self.selectMailbox(mailbox)
            self.mailbox = self.tell()
        elif mailbox != self.tell():
            self.selectMailbox(mailbox)
            self.mailbox = self.tell()
        
        if type(uid_list) != list:
            uid_list = [uid_list]

        '''
        for item in uid_list:
            msg=self.getMessage(item)
            print self.mailbox,msg.From,msg.Subject
        '''

        uid_list = str(uid_list).replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
        if var == 'body':
            f = self.server.imap_server.uid('FETCH', uid_list , '(BODY[TEXT])')
            msg_body = []
            if str(f[1]) != '[None]':
                for fm in f[1]:
                    if (len(fm) > 1):
                        msg_body.append(fm[1])
            return msg_body
        

    def process(self, mailbox, var):
        self.mailbox = mailbox
        self.messages = list()
        self.fetch_list = ''
        
        if(not self.server.loggedIn):
            self.server.login()
        
        result, message = self.server.imap_server.select(mailbox, readonly=1)
        if result != 'OK':
            return "error"  # raise Exception, message
        if type(var) == str:
            var = [var]
        if var[0] == 'all' or var[0] == 'all_body' or var[0] == 'all_attachments':
            searchType = (None, '(UNDELETED)')
            fetchType = var[0]
        elif var[0] == 'header':
            searchType = (None, '(HEADER ' + var[1] + ')')
            fetchType = 'all'
        elif var[0] == 'field':
            searchType = (None, '(' + var[1] + ' "' + var[2] + '")')
            fetchType = 'all'
        elif var[0] == 'msgID':
            searchType = (None, '(UNDELETED)')
            fetchType = 'msgID'
        elif var[0] == 'body':
            searchType = (None, '(UNDELETED)')
            fetchType = var[0]
        
        typ, data = self.server.imap_server.search(searchType[0], searchType[1])
        fetch_list = string.split(data[0])[-10:]  # limit to N most recent messages in mailbox, this is where pagination should be implemented
        self.fetch_list = ','.join(fetch_list)
        # print '1--',self.fetch_list
        msg_count = len(string.split(data[0]))
        if msg_count <= 10:
            fetch_results = self.fetch(mailbox, fetchType)
        else:
            iter_num = int(msg_count // 10.0)
            if str(complex(msg_count / 10.0))[1:str(complex(msg_count / 10.0)).find('+')].count('.') != 0:
                iter_num = iter_num + 1
            # print 'iter_num--',iter_num
            for i in range(1, iter_num):
                fetch_list = string.split(data[0])[-10 * (i + 1):-10 * i]  # limit to N most recent messages in mailbox, this is where pagination should be implemented
                fetch_list = ','.join(fetch_list)
                self.fetch_list = self.fetch_list + ',' + fetch_list
                # print self.fetch_list
            # print '2--',self.fetch_list
            self.fetch_list = self.fetch_list.rstrip(',')
            fetch_results = self.fetch(mailbox, fetchType)

        if fetchType == 'msgID':
            return fetch_results
        else:
            return self.messages
                    

    def __repr__(self):
        return "<gmail_messages:  \n%s\n>" % (self.messages)
    

    def __getitem__(self, key): return self.messages[key]

    def __setitem__(self, key, item): self.messages[key] = item
    

    def getMessage(self, uid):
        if(not self.server.loggedIn):
            self.server.login()
        self.server.imap_server.select(self.mailbox)
        
        status, data = self.server.imap_server.uid('fetch', uid, 'RFC822')
        
        messagePlainText = ''
        messageHTML = ''
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                for part in msg.walk():
                    if str(part.get_content_type()) == 'text/plain':
                        messagePlainText = messagePlainText + str(part.get_payload())
                    if str(part.get_content_type()) == 'text/html':
                        messageHTML = messageHTML + str(part.get_payload())
        
        # print data
        # create new message object
        message = gmail_message.gmail_message()
        
        if(messageHTML != ''):
            message.Body = messageHTML
        else:
            message.Body = messagePlainText
        if('Subject' in msg):
            message.Subject = msg['Subject']
        message.From = msg['From']
        message.uid = uid
        message.mailbox = self.mailbox
        message.date = msg['Date']
        return message
    
    

    def getAttachments(self, mailbox, detach_dir, msgVars, overright=False):
        msgUIDs, dates, senders = msgVars
        error_count = 0
        # if overright == False:
            # saved_files=os.listdir(detach_dir)
        self.selectMailbox(mailbox)
        # print mailbox
        f = self.server.imap_server.select(mailbox, readonly=1)
        msgs = range(1, len(msgUIDs) + 1)
        # print 'total messages:',len(msgUIDs)
        print 'total messages:', len(msgs)
        # for it in msgUIDs:
        msgData, copies = [], []
        for it in msgs:
            resp, data = self.server.imap_server.fetch(it, "(RFC822)")
            # print resp
            # print data
            # print(data[0])
            # try:
            email_body = data[0][1]  # getting the mail content
            mail = email.message_from_string(email_body)  # parsing the mail content to get a mail object
            # Check if any attachments at all
            # print mail.get_content_maintype()
            if mail.get_content_maintype() != 'multipart':
                continue
            for part in mail.walk():
                # multipart are just containers, so we skip them
                if part.get_content_maintype() == 'multipart':
                    continue
                # is this part an attachment ?
                if part.get('Content-Disposition') is None:
                    continue
                x = part.get_filename()
                filename = x
                counter = 1
                # print dates[it-1]+'\t'+senders[it-1]+'\t'+filename
                msgData.append(dates[it - 1] + '\t' + '\t' + senders[it - 1] + '\t' + filename)
                # break
                # '''
                
                # if there is no filename, we create one with a counter to avoid duplicates
                if not filename:
                    x = 'part-%03d%s' % (counter, 'bin')
                    filename = x
                    counter += 1
                att_path = os.path.join(detach_dir, filename)
                # Check if its already there
                if not os.path.isfile(att_path) :
                    # finally write the stuff
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                else: copies.append('copy' + dates[it - 1] + '\t' + '\t' + senders[it - 1] + '\t' + filename)
                
                # '''
                
            # except:
                # print msgUIDs.index(it)
                # print it,data[0]
                # error_count+=1
        for it in copies: print it
        print error_count
        print counter
        print ''
        for it in msgData:
            print it
        print ''
        if error_count != 0:
            x = os.listdir(detach_dir)
            if x.count('.DS') != 0: 
                # print x[x.index('.DS')]
                x.pop(x.index('.DS'))
            y = []
            for it in x:
                y.append(eval(it[:-4].split('_')[0]))
            y.sort()
            pt = 0
            print "y[i+1] - y[i], y[i]+pt , y[i], pt"
            for i in range(0, len(y) - 2):
                print y[i + 1] - y[i], y[i] + pt, y[i], pt
                if y[i + 1] - y[i] != 1:
                    print y[i + 1] - y[i], y[i] + pt, y[i], pt 
                    if y[i + 1] - y[i] == 2:
                        print '2--', y[i] + pt, y[i], pt
                        pt += 1
                        error_count -= -1
            if error_count == 0: return 'complete'

    def delMessage(self, mailbox, uid_list):
        if self.mailbox == mailbox: pass
        else: 
            # b=gmail_mailboxes.gmail_mailboxes(mailbox)
            self.mailbox == self.selectMailbox(mailbox)
        
        if type(uid_list) != list:
            uid_list = [uid_list]

        '''
        for item in uid_list:
            msg=self.getMessage(item)
            print self.mailbox,msg.From,msg.Subject
        '''

        uid_list = str(uid_list).replace('[', '').replace(']', '').replace("'", '').replace(' ', '')

        status, data = self.server.imap_server.uid('STORE', uid_list , '+FLAGS', '\\Deleted')
        print status
        print uid_list
        print asdsa
        self.server.imap_server.expunge()

    def copyMessage(self, src_folder_name, msg_uid, desti_folder_name):
        obj = self.server.imap_server
        obj.select(src_folder_name)
        apply_lbl_msg = obj.uid('COPY', msg_uid, desti_folder_name)
        if apply_lbl_msg[0] == 'OK':
            mov, data = obj.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
            obj.expunge()

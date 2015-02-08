import email, string
import gmail_imap

class gmail_message:

    def __init__(self):
    
        self.id = None
        self.uid = None
        self.flags = None
        self.mailbox = None
        self.msgID = None
        self.msgRef = None
        self.ReplyTo = None
        self.date = None
        self.From = None
        self.To = None
        self.Subject = '( no subject )'
        self.Body = None
        self.attachments = None
        
    def __repr__(self):
        str = "<gmail_message:  ID: %s  UID: %s Flags: %s Mailbox: %s \n" % (self.id, self.uid, self.flags, self.mailbox)
        str += "Message-ID: %s References: %s In-Reply-To: %s \n" % (self.msgID, self.msgRef, self.ReplyTo)
        str += "Date: %s From: %s To: %s Subject: %s \n" % (self.date, self.From, self.To, self.Subject)
        str += "Attachments: %s \n" % (self.attachments)
        str += "body: %s  >" % (self.Body)
        return str
    
    
